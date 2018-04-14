import os
import os.path

from setuptools import setup

name = 'autosuspend'

with open(os.path.join(
        os.path.abspath(os.path.dirname(os.path.realpath(__file__))),
        'VERSION'), 'r') as version_file:
    lines = version_file.readlines()
release = lines[1].strip()

setup(
    name=name,
    version=release,

    description='A daemon to suspend your server in case of inactivity',
    author='Johannes Wienke',
    author_email='languitar@semipol.de',
    license='GPL2',

    zip_safe=False,

    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'psutil>=5.0',
    ],
    extras_require={
        'Mpd': ['python-mpd2'],
        'Kodi': ['requests'],
        'XPath': ['lxml', 'requests'],
        'Logind support': ['dbus-python'],
    },
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-mock',
    ],

    scripts=[
        'autosuspend'
    ],
    data_files=[
        ('etc', ['autosuspend.conf',
                 'autosuspend-logging.conf']),
        ('lib/systemd/system', ['autosuspend.service',
                                'autosuspend-detect-suspend.service'])
    ],
)
