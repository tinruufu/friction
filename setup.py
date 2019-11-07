# coding=utf-8

import os
from setuptools import setup
from sys import version_info

if version_info.major != 3 or version_info.minor < 5:
    raise RuntimeError('friction requires python 3.5 or newer')

setup(
    name='friction',
    version='0.9',
    description=(
        'a browser-based gallery viewer tailored for viewing large '
        'collections of pornographic manga'
    ),
    long_description=(
        'please visit the homepage: https://github.com/tinruufu/friction'
    ),
    long_description_content_type='text/markdown',
    url='https://github.com/tinruufu/friction',
    author='ティン・ルーフ',
    author_email='tinruufu+pypi@gmail.com',
    packages=['friction'],
    scripts=[
        os.path.join('scripts', 'friction'),
        os.path.join('scripts', 'friction-ui'),
    ],
    app=[
        os.path.join('scripts', 'friction-ui'),
    ],
    license='MIT',
    platforms=['any'],
    install_requires=[
        'flask>=0.11,<0.12',
        'pillow',
        'python-magic',
        'rarfile',
    ],
    setup_requires=[
        'py2app',
    ],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    include_package_data=True,
    options={
        'py2app': {
            'iconfile': 'scripts/icon.icns',
            'plist': {
                'NSHumanReadableCopyright': '©2016 ティン・ルーフ',
            },
        }
    },
)
