from setuptools import setup, find_packages

setup(
    name="A",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25,<3.0",
    ],
)
