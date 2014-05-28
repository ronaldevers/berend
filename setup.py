from setuptools import find_packages, setup

setup(
    name='berend',
    packages=find_packages('.'),
    version='0.4',
    author='Ronald Evers',
    author_email='ronald@ch10.nl',
    url='https://github.com/ronaldevers/berend',
    description='Extensible IRC bot',
    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'Flask >= 0.10.0',
        'pyopenssl >= 0.13.0',
        'pyyaml >= 3.10',
        'twisted >= 13.0.0',
    ],
    entry_points={
        'console_scripts': [
            'berend = berend.noapi:main',
        ],
    },
)
