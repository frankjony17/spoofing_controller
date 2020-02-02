# -*- encoding: utf-8 -*-
# Source:
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    'bandit',
    'flake8',
    'isort',
    'pytest',
]
unit_test_requirements = [
    'pytest',
]
integration_test_requirements = [
    'pytest',
]
run_requirements = [
    'flask', 'gunicorn', 'flask-swagger-ui', 'pyyaml', 'pydantic==0.32.2',
    'prometheus_client', 'requests', 'aiohttp'
]

with io.open('./nia_sauron_spoofing_controller/__init__.py', encoding='utf8') \
        as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="nia-sauron-spoofing-controller",
    version=version,
    author="Frank Ricardo Ramirez",
    author_email="c1310169@interno.bb.com.br",
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    url="https://fontes.intranet.bb.com.br/nia/nia-sauron-spoofing-controller/"
        "nia-sauron-spoofing-controller",
    license="COPYRIGHT",
    description="Check if an image is taken from another image or from the "
                "real world. Consume the antispoofing APIs and return a final"
                " answer",
    long_description=long_description,
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         'dev': dev_requirements,
         'unit': unit_test_requirements,
         'integration': integration_test_requirements,
    },
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=(),
    entry_points={
        'console_scripts': [
            'nia_sauron_spoofing_controller ='
            ' nia_sauron_spoofing_controller.main:app'
        ],
    },
)
