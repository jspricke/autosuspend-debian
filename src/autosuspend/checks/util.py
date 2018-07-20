import configparser
from typing import Any, Dict, Iterable, Optional

from . import ConfigurationError, SevereCheckError, TemporaryCheckError


class CommandMixin:
    """Mixin for configuring checks based on external commands."""

    @classmethod
    def create(cls, name: str, config: configparser.SectionProxy):
        try:
            return cls(name, config['command'].strip())  # type: ignore
        except KeyError as error:
            raise ConfigurationError(
                'Missing command specification') from error

    def __init__(self, command: str) -> None:
        self._command = command


class NetworkMixin:

    @classmethod
    def collect_init_args(
            cls, config: configparser.SectionProxy) -> Dict[str, Any]:
        try:
            args = {}  # type: Dict[str, Any]
            args['timeout'] = config.getint('timeout', fallback=5)
            args['url'] = config['url']
            args['username'] = config.get('username')
            args['password'] = config.get('password')
            if (args['username'] is None) != (args['password'] is None):
                raise ConfigurationError('Username and password must be set')
            return args
        except ValueError as error:
            raise ConfigurationError(
                'Configuration error ' + str(error)) from error
        except KeyError as error:
            raise ConfigurationError(
                'Lacks ' + str(error) + ' config entry') from error

    @classmethod
    def create(cls, name: str, config: configparser.SectionProxy):
        return cls(name, **cls.collect_init_args(config))  # type: ignore

    def __init__(self, url: str, timeout: int,
                 username: Optional[str] = None,
                 password: Optional[str] = None) -> None:
        self._url = url
        self._timeout = timeout
        self._username = username
        self._password = password

    def request(self):
        import requests
        from requests.auth import HTTPBasicAuth, HTTPDigestAuth
        import requests.exceptions

        auth_map = {
            'basic': HTTPBasicAuth,
            'digest': HTTPDigestAuth,
        }

        session = requests.Session()
        try:
            from requests_file import FileAdapter
            session.mount('file://', FileAdapter())
        except ImportError:
            pass

        try:
            reply = session.get(self._url, timeout=self._timeout)

            # replace reply with an authenticated version if credentials are
            # available and the server has requested authentication
            if self._username and self._password and reply.status_code == 401:
                auth_scheme = reply.headers[
                    'WWW-Authenticate'].split(' ')[0].lower()
                if auth_scheme not in auth_map:
                    raise SevereCheckError(
                        'Unsupported authentication scheme {}'.format(
                            auth_scheme))
                auth = auth_map[auth_scheme](self._username, self._password)
                reply = session.get(
                    self._url, timeout=self._timeout, auth=auth)

            reply.raise_for_status()
            return reply
        except requests.exceptions.RequestException as error:
            raise TemporaryCheckError(error) from error


class XPathMixin(NetworkMixin):

    @classmethod
    def collect_init_args(cls, config) -> Dict[str, Any]:
        from lxml import etree
        try:
            args = NetworkMixin.collect_init_args(config)
            args['xpath'] = config['xpath'].strip()
            # validate the expression
            try:
                etree.fromstring('<a></a>').xpath(args['xpath'])
            except etree.XPathEvalError as error:
                raise ConfigurationError(
                    'Invalid xpath expression: ' + args['xpath']) from error
            return args
        except ValueError as error:
            raise ConfigurationError(
                'Configuration error ' + str(error)) from error
        except KeyError as error:
            raise ConfigurationError(
                'Lacks ' + str(error) + ' config entry') from error

    @classmethod
    def create(cls, name: str, config: configparser.SectionProxy):
        return cls(name, **cls.collect_init_args(config))

    def __init__(self, xpath: str, **kwargs) -> None:
        NetworkMixin.__init__(self, **kwargs)
        self._xpath = xpath

    def evaluate(self) -> Iterable[Any]:
        import requests
        import requests.exceptions
        from lxml import etree

        try:
            reply = self.request().content
            root = etree.fromstring(reply)
            return root.xpath(self._xpath)
        except requests.exceptions.RequestException as error:
            raise TemporaryCheckError(error) from error
        except etree.XMLSyntaxError as error:
            raise TemporaryCheckError(error) from error
