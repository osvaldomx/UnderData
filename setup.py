import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="underdata",
    version="0.1.2",
    author="osvaldomx",
    author_email="osvaldo.trujillo.ingenieria@gmail.com",
    description="Scraping data package for www.understat.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/osvaldomx/UnderData",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=["requests>=2.26.0", "selenium>=4.0.0", "pandas>=1.3.4"],
    python_requires = ">=3.6",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ]
)