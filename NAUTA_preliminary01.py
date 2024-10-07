
import os
import re
import PIL
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from numbers import Number
from numpy.fft import rfft
from scipy.io.wavfile import read as wavread

## NAUTA

class NAUTA():
    '''
    NAUTA base class.
    
    NAUTA class must not be instantiated. Subclasses should implement a constructor
    at minimum. Constructors of derived classes are responsible for getting the
    raw audio data into self.signal
    
    See WavNAUTA, RawNAUTA for concrete classes implementing the NAUTA.
    '''
    
    def __init__(self):
        if type(self) is NAUTA:
            raise NotImplementedError("NAUTA is an abstract class and cannot be instantiated directly.")
            
    # Methods from tryan/LTSA adapted to Python.3 (GitHub: https://github.com/tryan/LTSA)
    
    def _init_ltsa_params(self):
        '''
        Initialize some useful attributes with default values to compute LTSA and use the plot_ltsa() and 
        crop_ltsa() methods. The default values can be replaced using set_ltsa_params(). This method must 
        be executed by the constructor once the signal data and sample rate have been filled. 
        '''
        # Defaults parameters for the LTSA algorithm
        self.div_len = int(np.round(self.fs/2)) # half second divisions
        self.subdiv_len = int(2**np.round(np.log2(self.fs/5)))
        self.nfft = None # will be checked and assigned in the compute_lsta() method
        self.noverlap = 0
        self.norm_scal_process = []

        self._set_ltsa_nvals()
        
        # Default time and frequency limits, used for displaying results
        self.tmin = 0
        self.tmax = np.floor(self.nsamples / self.fs)
        self.fmin = 0
        self.fmax = np.floor(self.fs / 2)
        
    def set_ltsa_params(self, params_dict):
        '''
        Allows the user to set custom values for the Long Term Spectral Average (LTSA) calculation parameters
        described by the Scripps Institute of Oceanography and implemented by: https://github.com/tryan/LTSA
        It is recommended that only these variables be manipulated: div_len, subdiv_len, nfft, and noverlap.
        
        Parameters:
            
            - div_len: FALTA DESCRIPCIÓN...
            - subdiv_len: FALTA DESCRIPCIÓN...
            - nfft: FALTA DESCRIPCIÓN...
            - noverlap: FALTA DESCRIPCIÓN...
        '''
        for key, val in params_dict.items(): # for Python2 replace items() with iteritems() !
            vars(self)[key] = val

        self._set_ltsa_nvals()
    
    def _set_ltsa_nvals(self):
        '''
        Computes and sets the nsamples, ndivs, and nsubdivs attributes used for the LTSA algorithm. Ths function
        is used by _init_ltsa_params() and set_ltsa_params().
        '''
        self.nsamples = self.signal.size
        self.ndivs = int(np.floor(self.nsamples / self.div_len))
        self.nsubdivs = int(np.floor(self.div_len / (self.subdiv_len - self.noverlap)))
        
    def compute_ltsa(self):
        '''
        This method executes the Long Term Spectral Average (LTSA) described by the Scripps Institute of 
        Oceanography and implemented by: https://github.com/tryan/LTSA. The result is a grayscale image (2D 
        numpy array) which is assigned to the self.ltsa attribute.
        Select custom parameters for the LTSA calculation using set_ltsa_params() otherwise the default 
        parameters will be used.
        '''
        if self.nfft is None:
            self.nfft = int(self.subdiv_len)
        self.signal = self.signal[: self.ndivs * self.div_len]
        self.tmax = len(self.signal) / self.fs
        self.ltsa = np.zeros((self.nfft//2, self.ndivs), dtype=np.single)
        divs = np.reshape(self.signal, (self.ndivs, self.div_len)).T
        for i in range(int(self.ndivs)): # for Python2 replace range() with xrange() !
            div = divs[:,i]
            self.ltsa[:,i] = self._calc_ltsa_spectrum(div)
            
        #return self.ltsa
    
    def _calc_ltsa_spectrum(self, div):
        '''
        This function is used by compute_ltsa() to determine the approximate frequency content (spectrogram) of a 
        split of audio data.
        '''
        spectrum = np.zeros((self.nfft//2,))
        window = np.hanning(self.subdiv_len)
        slip = self.subdiv_len - self.noverlap
        if slip <= 0:
            raise ValueError('overlap exceeds subdiv_len, slip = %s' % str(slip))
        lo = 0
        hi = self.subdiv_len
        nsubdivs = 0
        while hi < self.div_len:
            nsubdivs += 1
            subdiv = div[lo:hi]
            tr = rfft(subdiv * window, int(self.nfft))
            spectrum += np.abs(tr[:self.nfft//2])
            lo += slip
            hi += slip

        spectrum = np.single(np.log(spectrum / self.nsubdivs))
        return spectrum
    
    def scale_ltsa_to_uint8(self): 
        '''
        Rescales self.ltsa to fit into unsigned 8-bit integers and converts the data type of self.ltsa to np.uint8.
        '''
        # Scales the LTSA matrix if it has not been scaled previously
        if self.ltsa_norm_stat==False:
            self.ltsa -= self.ltsa.min()
            self.ltsa *= 255 / self.ltsa.max()
            self.ltsa = np.uint8(self.ltsa)
        # Register the processing status
        self.ltsa_scal_stat = True
        self.ltsa_norm_scal_process.append("S")
    
    def normalize_ltsa(self, normrange=[0,1]):
        '''
        Normalise self.ltsa (defaults to range 0-1) if not done previously. It also updates the normalisation status 
        `ltsa_norm_stat` to `True` and records the operation in the `ltsa_norm_scal_process` attribute.
        '''        
        if self.ltsa_scal_stat==False:
            arr_min = np.min(self.ltsa)
            arr_max = np.max(self.ltsa)
            arr_norm = (self.ltsa - arr_min) / (arr_max - arr_min)
            range_min, range_max = normrange
            self.ltsa = arr_norm * (range_max - range_min) + range_min
        # Register the processing status
        self.ltsa_norm_stat = True
        self.ltsa_norm_scal_process.append("N")
    
    def plot_ltsa(self, resize=None, interp='bilinear'):
        '''
        FALTA DOCUMENTAR Y COMENTAR
        '''
        if not hasattr(self, 'ltsa'):
            self.compute_ltsa()
        
        if isinstance(resize, tuple) and len(resize) == 2:
            pimg = PIL.Image.fromarray(self.ltsa) # img = imresize(self.ltsa, resize, interp)
            pimg = pimg.resize(resize, resample=interp)
            img = np.asarray(pimg)
        
        elif isinstance(resize, int):
            if resize < 1 or resize > self.ltsa.shape[0]:
                raise ValueError('resize out of range: %s' % str(resize))

            h = resize # img height in pixels
            idx = np.floor(np.linspace(0, np.size(self.ltsa, 0)-1, h))
            idx = np.int32(idx)
            img = np.zeros((h, np.size(self.ltsa, 1)))
            for i in range(int(np.size(self.ltsa, 1))): # for Python2 replace range() with xrange() !
                img[:,i] = self.ltsa[idx,i]
        
        elif resize is None:
            img = self.ltsa

        else:
            raise TypeError('resize not of acceptable type: %s' % str(resize))
        
        ext = (self.tmin, self.tmax, self.fmin, self.fmax)
        self.handle = plt.imshow(img, origin='lower', extent=ext, aspect='auto')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Frequency (Hertz)')

        #return img
    
    def plot_waveform(self):
        '''
        Plots the waveform of the audio signal.
        '''
        if not hasattr(self, 'signal') or self.signal is None:
            raise ValueError('No audio signal available to plot.')
    
        time = np.linspace(0, len(self.signal) / self.fs, num=len(self.signal))
    
        plt.figure(figsize=(10, 4))
        plt.plot(time, self.signal)  # Plot the signal amplitude against time
        plt.title('Waveform')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.grid(True)  # Optional: add a grid for better visibility
        plt.show()
  
    def crop_ltsa(self, tmin=0, tmax=None, fmin=0, fmax=None):
        '''
        FALTA DOCUMENTAR Y COMENTAR
        '''
        if tmax is None:
            tmax = self.tmax
        if fmax is None:
            fmax = self.fmax

        inputs = [tmin, tmax, fmin, fmax]
        for val in inputs:
            if not (isinstance(val, Number) and np.isreal(val)):
                raise TypeError('all inputs must be real numbers')

        if tmin < self.tmin or tmax <= tmin or tmax < 0:
            raise ValueError('tmin (%.3f) and/or tmax (%.3f) out of range' % (tmin, tmax))
        if fmin < self.fmin or fmax <= fmin or fmax < 0:
            raise ValueError('fmin (%.3f) and/or fmax (%.3f) out of range' % (fmin, fmax))

        self.tmin = tmin
        self.tmax = tmax
        self.fmin = fmin
        self.fmax = fmax

        divs_per_second = self.fs / self.div_len
        div_low = int(np.floor(tmin * divs_per_second))
        div_high = int(np.ceil(tmax * divs_per_second)) + 1
        self.ltsa = self.ltsa[:, div_low:div_high]

        pixels_per_hz = self.ltsa.shape[0] / (self.fs/2)
        freq_low = int(np.floor(fmin * pixels_per_hz))
        freq_high = int(np.ceil(fmax * pixels_per_hz)) + 1
        self.ltsa = self.ltsa[freq_low:freq_high, :]

        return div_low, div_high, freq_low, freq_high
       
    # AQUÍ FALTAN LOS MÉTODOS PROPIOS...

## WavNAUTA

class WavNAUTA(NAUTA):
    '''
    WavNAUTA is a subclass of NAUTA that handles WAV file audio data.
    '''
    
    def __init__(self, _file, channel=0): 
        # Ensure that NAUTA is not instantiated directly
        super().__init__()       
        # Initial attributes from name and create empty attributes
        self.object_class = "WavNAUTA"
        self.filename = os.path.basename(_file)
        self.directory = os.path.dirname(_file)
        self.device_id, self.date_str, self.time_str = self._extract_attributes_from_wav_filename(self.filename)
        self.start_timestamp = self._generate_timestamp(self.date_str, self.time_str)
        self.datetime = self._generate_datetime(self.start_timestamp)       
        
        # Read the WAV file
        if isinstance(_file, str) and _file.endswith('.wav'):
            self.fs, self.signal = wavread(_file)
            if self.signal.ndim > 1:
                self.signal = self.signal[:, channel]  # Take only one channel
        else:
            raise TypeError(f'Input is not a path to a .wav file: {_file}')
        
        self.duration = len(self.signal) / self.fs # seconds
        self.end_timestamp = self.start_timestamp + timedelta(seconds=self.duration)
        
        # Initialize LTSA defauolt attributes
        self._init_ltsa_params()
        
    def _extract_attributes_from_wav_filename(self, filename):
        # Remove the file extension
        name_without_extension = os.path.splitext(filename)[0]
        
        # Use a regular expression to extract the device_id, date, and time
        match = re.match(r"([a-zA-Z0-9]+)_([0-9]{8})_([0-9]{6})", name_without_extension)
        if match:
            device_id = match.group(1)
            date_str = match.group(2)
            time_str = match.group(3)
            return device_id, date_str, time_str
        else:
            raise ValueError(f"Filename '{filename}' does not match the expected pattern.")
    
    def _generate_timestamp(self, date_str, time_str):
        # Convert date and time strings to a datetime object
        try:
            date_time_str = f"{date_str} {time_str}"
            timestamp = datetime.strptime(date_time_str, "%Y%m%d %H%M%S")
            return timestamp
        except ValueError as e:
            raise ValueError(f"Error parsing date and time: {e}")
            
    def _generate_datetime(self, timestamp):
        # Convert the datetime object to a formatted string
        return timestamp.strftime("%Y/%m/%d %H:%M:%S")
  
## RawNAUTA

class RawNAUTA(NAUTA):
    '''
    RawNAUTA is a subclass of NAUTA for handling raw audio data.
    '''
    pass

## Tools:

def add_device_id(input_path, device_id):
    """
    Adds a user-defined prefix to a .wav file, a list of .wav files, or all .wav files in a specified folder. Useful
    to add the device_id when it is not defined by default.

    :param input_path: Absolute path to a .wav file, a list of absolute paths to .wav files,
                       or a folder path containing .wav files.
    :param device_id: String that will be added as a prefix to the name of each file.
    """
    # Check if input_path is a directory
    if os.path.isdir(input_path):
        # If it is a directory, iterate over the .wav files in it
        for filename in os.listdir(input_path):
            if filename.endswith('.wav'):
                original_file = os.path.join(input_path, filename)
                new_filename = f"{device_id}_{filename}"
                new_file = os.path.join(input_path, new_filename)
                os.rename(original_file, new_file)
                print(f"Renamed: {filename} to {new_filename}")

    # Check if input_path is a single file
    elif os.path.isfile(input_path) and input_path.endswith('.wav'):
        original_file = input_path
        filename = os.path.basename(original_file)
        new_filename = f"{device_id}_{filename}"
        new_file = os.path.join(os.path.dirname(original_file), new_filename)
        os.rename(original_file, new_file)
        print(f"Renamed: {filename} to {new_filename}")

    # Check if input_path is a list of files
    elif isinstance(input_path, list):
        for file_path in input_path:
            if os.path.isfile(file_path) and file_path.endswith('.wav'):
                original_file = file_path
                filename = os.path.basename(original_file)
                new_filename = f"{device_id}_{filename}"
                new_file = os.path.join(os.path.dirname(original_file), new_filename)
                os.rename(original_file, new_file)
                print(f"Renamed: {filename} to {new_filename}")
            else:
                print(f"Warning: {file_path} is not a valid .wav file or does not exist.")
    else:
        print("Error: The provided argument is neither a folder, a .wav file, nor a valid list of .wav files.")

def remove_fs_str(input_path):
    """
    Removes the last three characters from the filename (excluding the extension),
    along with the last underscore (_), for a given .wav file, a list of .wav files,
    or all .wav files in a specified folder.

    :param input_path: Absolute path to a .wav file, a list of absolute paths to .wav files,
                       or a folder path containing .wav files.
    """
    # Check if input_path is a directory
    if os.path.isdir(input_path):
        # If it is a directory, iterate over the .wav files in it
        for filename in os.listdir(input_path):
            if filename.endswith('.wav'):
                file_path = os.path.join(input_path, filename)
                _rename_file(file_path)

    # Check if input_path is a single file
    elif os.path.isfile(input_path) and input_path.endswith('.wav'):
        _rename_file(input_path)

    # Check if input_path is a list of files
    elif isinstance(input_path, list):
        for file_path in input_path:
            if os.path.isfile(file_path) and file_path.endswith('.wav'):
                _rename_file(file_path)
            else:
                print(f"Warning: {file_path} is not a valid .wav file or does not exist.")
    else:
        print("Error: The provided argument is neither a folder, a .wav file, nor a valid list of .wav files.")

def _rename_file(file_path):
    """
    Helper function to remove the last three characters from the filename
    (excluding the extension) and the last underscore (_) of a given .wav file.

    :param file_path: Absolute path to the .wav file.
    """
    if os.path.isfile(file_path) and file_path.endswith('.wav'):
        # Extract the directory and the filename
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        # Split the filename and extension
        name, ext = os.path.splitext(filename)

        # Check if the name is long enough to remove three characters
        if len(name) > 3:
            # Remove the last three characters
            new_name = name[:-3]

            # Remove the last underscore if it exists
            if new_name.endswith('_'):
                new_name = new_name[:-1]

            new_name += ext  # Add the original extension back
            new_file_path = os.path.join(directory, new_name)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} to {new_name}")
        else:
            print(f"Error: The filename '{filename}' is too short to remove three characters.")
    else:
        print(f"Error: The provided path '{file_path}' is not a valid .wav file.")
