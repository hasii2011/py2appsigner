import pathlib
from setuptools import setup

from py2appsigner import __version__ as version
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README  = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="py2appsigner",
    version=version,
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Scripts to Code Sign py2app applications',
    long_description=README,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url="https://github.com/py2appsigner",
    packages=[
        'py2appsigner',
        'py2appsigner.environment',
        'py2appsigner.resources',
    ],
    package_data={
        'py2appsigner.resources': ['loggingConfiguration.json'],
    },

    install_requires=[
        'click~=8.1.3', 'tqdm==4.65.0'
    ],
    entry_points={
        "console_scripts": [
            "py2appSign=py2appsigner.Commands:py2appSign",
            "appNotarize=py2appsigner.Commands:appNotarize",
            "appStaple=py2appsigner.Commands:appStaple",
            "appVerify=py2appsigner.Commands:appVerify",
            "notaryTool=py2appsigner.Commands:notaryTool",
        ]
    },
)
