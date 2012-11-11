from setuptools import setup

setup(
    name='botlerplate',
    py_modules=['botlerplate'],
    version='0.1',
    author='Ronald Evers',
    author_email='ronald@ch10.nl',
    url='https://github.com/ronaldevers/botlerplate',
    description='Boilerplate for Twisted IRC bots',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=['twisted'],
)
