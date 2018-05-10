"""A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pythonista_api_client',
    version='0.1.4',
    description='Making requests to rest apis in pythonista.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ephes/pythonista_api_client',
    author='Jochen Wersdoerfer',
    author_email='jochen-pythonista@wersdoerfer.de',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='api rest pythonista jwt token drf',  # Optional
    packages=find_packages(exclude=['examples', 'docs', 'tests']),
    install_requires=['requests'],
    extras_require={
        'dev': ['pytest', 'flake8'],
    },
)
