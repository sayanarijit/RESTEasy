from setuptools import setup, find_packages
from codecs import open
from os import path


VERSION = 'v1.0.0'

here = path.abspath(path.dirname(__file__))

# Get requirements from requirements.txt file
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RESTEasy',
    version=VERSION,
    description='REST API calls made easier',
    long_description=long_description,
    url='https://github.com/rapidstack/RESTEasy',
    download_url='https://github.com/rapidstack/RESTEasy/archive/%s.tar.gz' % VERSION,
    author='Arijit Basu',
    author_email='sayanarijit@gmail.com',
    license='MIT',
    py_modules=['resteasy'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft'
    ],
    keywords='REST API client',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements
)
