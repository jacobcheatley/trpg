from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    readme = f.read()

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='trpg',
    version='0.1.0',
    description='Simple text RPG engine for running custom JSON campaigns.',
    long_description=readme,
    url='https://github.com/jacobcheatley/trpg',
    author='Jacob Cheatley',
    author_email='jacobcheatley@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Gamers and Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='text roleplaying game engine',
    packages=find_packages(),
    package_data={
        'trpg': ['sample.trpg']
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'trpg=trpg.__main__:main'
        ]
    }
)