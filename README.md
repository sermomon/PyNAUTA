# pyNAUTA

Brief introduction to NAUTA class

https://www.nauta-rcs.it/IT/

![Imagen1](https://github.com/user-attachments/assets/b2debcf7-71eb-4853-8019-d0f8e0da6328)



```
import NAUTA

# Instance NAUTA object from a WAV file
file_path = "C:/Lab/projects/vessel_acoustic_signature/data/example/NAUTA/23d51_20240415_084603.wav"
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

## Required features:

1) `split()` como función fuera de la clase que reciba un objeto de tipo *WavNAUTA* o *RawNAUTA*
2) crear vectores de tiempo y frecuencia del ltsa: `self.ltsa_freq`, `self.ltsa_time`
