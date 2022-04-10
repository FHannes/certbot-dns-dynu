import os

from setuptools import setup
from setuptools import find_packages

version = "0.1.0"

with open('README.md') as f:
    long_description = f.read()

install_requires = [
    'acme>=1.26.0',
    'certbot>=1.26.0',
    'dns-lexicon>=3.9.4',
    'dnspython',
    'mock',
    'setuptools>=41.6.0',
    'requests'
]

if not os.environ.get('SNAP_BUILD'):
    install_requires.extend([
        'acme>=1.26.0',
        'certbot>=1.26.0',
    ])
else:
    install_requires.append('packaging')

setup(
    name='certbot-dns-dynu',
    version=version,

    description="Dynu DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bikram990/certbot-dns-dynu',
    download_url=f'https://github.com/bikram990/certbot-dns-dynu/archive/refs/tags/{version}.tar.gz',
    author="Bikramjeet Singh",
    license='Apache License 2.0',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-dynu = certbot_dns_dynu._internal.dns_dynu:Authenticator',
        ],
    },
)
