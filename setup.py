
from setuptools import setup, find_packages

setup(
    name="pyNAUTA",
    version="0.1.0",
    description="Software tools for data management and analysis of Acoustic Passive Monitoring Systems data captured by NAUTA scientific recorders.",
    author="Sergio Morell-Monzó",
    author_email="sermomon@upv.es",
    url="https://github.com/sermomon/pyNAUTA",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'NAUTA': ['23d51_20240415_084603e.wav'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

