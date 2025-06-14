from setuptools import setup, find_packages

setup(
    name='sva2-authenticator',
    version='0.1',
    packages=find_packages(include=[
        'sva2_cli', 'sva2_cli.*',
        'totp_authenticator', 'totp_authenticator.*'
    ]),
    install_requires=[
        'pyotp',
        'qrcode',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'sva2 = sva2_cli.main:main',
        ],
    },
)
