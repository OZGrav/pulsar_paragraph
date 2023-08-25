import os

def get_data_path(file_name):
    return os.path.join(os.path.dirname(__file__), 'data_files', file_name)