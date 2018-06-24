import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="termapp",
    version="0.0.1",
    author="Marco A. Pagliaricci",
    author_email="mark@spinloops.com",
    description="Terminal command-line page application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://spinloops.com",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

