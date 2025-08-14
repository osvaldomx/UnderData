import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="underdata",
    version="0.2.0",
    author="Osvaldo Trujillo",
    author_email="osvaldo.trujillo.ingenieria@gmail.com",
    description="Scraping data package for www.understat.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/osvaldomx/UnderData",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=["requests==2.32.3", "beautifulsoup4==4.12.3", "pandas==2.2.2"],
    python_requires = ">=3.13",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent'
    ]
)