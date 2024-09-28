# PyNAUTA 🌊🎙️🌍 💻 


Software tools for data management and analysis of Acoustic Passive Monitoring Systems data captured by NAUTA scientific recorders. This tool has been developed by the Underwater Acoustics Group of the Applied Physics Department of the Universitat Politècnica de València, but it is open to new contributors.

NAUTA scientific: https://www.nauta-rcs.it/IT/

### Installation

Binary installers are available at the Python Package Index ([PyPI](https://pypi.org/project/PyNAUTA)).

```
pip install PyNAUTA
```

### Main Features

### Getting started

After installing the PyNAUTA library you can import it as follows:

```
import PyNAUTA
```

The recordings made by NAUTA scientific instruments are stored in Waveform File Format (WAV) files with the following structure `<device_id_yyyymmdd_hhmmss.wav>`. You can instantiate a NAUTA object from the `WavNAUTA()` constructor:

```
# Instance a new NAUTA (WavNAUTA) object

rec = WavNAUTA('C:/data/NAUTA/23d51_20240415_084603.wav')
```

If you do not already have a recording taken by a NAUTA scientific device, a sample recording is included in the package and can be accessed as follows:

```
# Load example data

rec = load_nauta_example()
```

NAUTA objects (WavNAUTA) are initialized with some default attributes. For example, the filename, the source directory, the device ID, the start date and time of the recording, the start and end timestamp, or the duration of the recording:

```
# Get some useful information from a NAUTA (WavNAUTA) object

print('Filename: ', rec.filename)
print('Source directory :', rec.directory)
print('Device ID:', rec.device_id)
print('Date and time: ', rec.datetime)
print('Start timestamp: ', rec.start_timestamp)
print('End timestamp: ', rec.end_timestamp)
print('Recording duration: ', rec.duration, '[sec.]')
```

Of course, the sample rate and the number of samples can also be accessed:

```
print('Sampling rate :', rec.fs)
print('Number of samples :', rec.samples) #!
```

The recorded signal is stored in the signal attribute. It is possible to access the signal and display the waveform as follows:

```
# Access to the signal
rec.signal

# Plot waveform
rec.plot_waveform()
```

### Documentation
...
...
...

### Contributions Welcome
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](#)

If you find any bug in the code or have any improvements in mind then feel free to generate a pull request.

## Required features:

1) `split()` como función fuera de la clase que reciba un objeto de tipo *WavNAUTA* o *RawNAUTA* y recorte el archivo.
2) `join()` como función fuera de la clase que reciba una lista de *WavNAUTA* o *RawNAUTA* para unir archivos consecutivos.
3) `fusion()` como función fuera de la clase que reciba una lista de *WavNAUTA* o *RawNAUTA* para unir archivos NO consecutivos (artificial).
4) `rename_wav()` -mejorar el nombre- función fuera de la clase que reciba una lista de *WavNAUTA* o *RawNAUTA* y estandarice el nombre según <device_id_yyyymmdd_hhmmss.wav>.
5) `data_report()` como función fuera de la clase que reciba una carpeta y genere un report de los archivos disponibles y sus características.
6) crear dos atributos nuevos vectores de tiempo y frecuencia del ltsa: `self.ltsa_freq`, `self.ltsa_time`
7) crear métodos para calcular y graficar el SPL: `_init_spl_params()`, `set_spl_params()`, `compute_spl()`, `plot_spl()`.
8) crear metodo: `export_to_raw()` que guarde la señal y los atributos en un Zarr o similar que ocupe menos espacio.
9) crear métodos: `set_geographic_info()` y `show_on_map()` -mejorar nombre- que asigne unas cordenadas geográficas y sistema de referencia al archivo y permita visualizarlo en un mapa.
10) crear método: `save_metadata_to_wav()` que permita exportar el wav con todos los metadatos que se han cargado. En este caso solo la información geográfica y alguna cosa más que no se puede cargar automaticamente: sensibilidad, ganancia...
