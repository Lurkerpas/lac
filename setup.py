from setuptools import setup
from setuptools import find_packages

import lac

setup(
    name="lac",
    description="",
    version=lac.__version__,
    packages=find_packages(),
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