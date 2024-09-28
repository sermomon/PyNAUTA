# PyNAUTA 🌊🎙️🌍 

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

NAUTA objects (WavNAUTA) are initialized with some default attributes. For example, the filename, the source directory, the device id, the start date and time of the recording, the start and end timestamp, or the duration of the recording:

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












```
import NAUTA

# Instance NAUTA object from a WAV file
file_path = "C:/NAUTA/23d51_20240415_084603.wav"
record = WavNAUTA(file_path)

# Get file info
record.filename
record.directory
record.device_id
record.date_str
record.time_str

# Get signal alf fs
record.fs
record.signal

# Get time info
record.datetime
record.start_timestamp
record.end_timestamp
record.duration

# Compute LTSA
hasattr(record, 'ltsa')
record.compute_ltsa()

# Plot LTSA
record.plot_ltsa()

```

### Contributions Welcome
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](#)

If you find any bug in the code or have any improvements in mind then feel free to generate a pull request.

## Required features:

1) `split()` como función fuera de la clase que reciba un objeto de tipo *WavNAUTA* o *RawNAUTA*
2) crear vectores de tiempo y frecuencia del ltsa: `self.ltsa_freq`, `self.ltsa_time`
3) modificar método `plot_waveform()` para que muestre el tiempo en lugar de las muestras en el eje X
