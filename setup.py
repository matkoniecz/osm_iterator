import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osm_iterator",
    version="0.0.5",
    author="Mateusz Konieczny",
    author_email="matkoniecz@gmail.com",
    description="Ierate over .osm file and call a provided callback function for each element",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkoniecz/osm_iterator",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
) 
