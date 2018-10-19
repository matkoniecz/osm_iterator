import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osm_iterator",
    version="1.0.0",
    author="Mateusz Konieczny",
    author_email="matkoniecz@gmail.com",
    description="Iterate over .osm file and call a provided callback function for each element",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkoniecz/osm_iterator",
    packages=setuptools.find_packages(),
    install_requires = [
        'lxml>=3.5.0, <4.0',
        'nose>=1.3.7, <2.0',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
