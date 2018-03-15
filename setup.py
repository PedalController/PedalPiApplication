# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path
from setuptools import setup


def readme():
    here = path.abspath(path.dirname(__file__))

    with open(path.join(here, 'README.rst'), encoding='UTF-8') as f:
        return f.read()

setup(
    name='PedalPi-Application',
    version='0.4.1',

    description='Framework for manager the Pedal Pi',
    long_description=readme(),

    url='https://github.com/PedalPi/Application',

    author='Paulo Mateus Moura da Silva (SrMouraSilva)',
    author_email='mateus.moura@hotmail.com',
    maintainer='Paulo Mateus Moura da Silva (SrMouraSilva)',
    maintainer_email='mateus.moura@hotmail.com',

    license="Apache Software License v2",

    packages=[
        'application',
        'application/component',
        'application/controller',
        'application/dao',

        'application/data',
        'application/data/banks',
        'application/data/components',
        'application/data/current',
    ],
    package_data={
        'application/data': ['*.json', '*/*.json'],
    },
    install_requires=['PedalPi-PluginsManager==0.7.*'],

    test_suite='test',
    tests_requires=['PedalPi-PluginsManager'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='pedal-pi mod-host lv2 audio plugins-manager',

    platforms='Linux',
)
