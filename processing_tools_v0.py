
import os
import re

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
