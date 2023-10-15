from setuptools import setup
from setuptools import find_packages

import lac

setup(
    name="lac",
    description="",
    version= "0.0.1",
    packages=find_packages(),
    package_data={"lac" : ["acn.lark","asn1.lark"]},
    data_files=[("lactemplates",["data/cheader.mako"])],
    author="Michał Kurowski",
    author_email="lurkerpas@gmail.com",
    url="https://github.com/Lurkerpas/lac",
    install_requires=["mako","pytest","pathlib","lark"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Linux, Windows"
    ],
    entry_points={
        'console_scripts': [
            'lac = lac.lac:main'
        ]
    }
)