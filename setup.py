
from setuptools import setup, find_packages

setup(
    name="pyNAUTA",  # Asegúrate de que este nombre sea único en PyPI
    version="0.1.0",  # Versión del paquete
    description="Herramientas para trabajar con datos acústicos de sistemas subacuáticos.",
    author="Sergio Morell-Monzó",
    author_email="sermomon@upv.es",
    url="https://github.com/sermomon/pyNAUTA",  # El repositorio donde está alojado tu código
    packages=find_packages(),  # Encuentra automáticamente los paquetes dentro del directorio
    include_package_data=True,  # Incluye archivos adicionales, como tu archivo WAV
    package_data={
        'NAUTA': ['data/example.wav'],  # Especifica los archivos de datos incluidos
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

