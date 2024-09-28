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
