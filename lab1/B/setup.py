from setuptools import setup, find_packages

setup(
    name="B",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.18,<2.25",
    ],
)
