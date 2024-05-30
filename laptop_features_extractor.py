import re
import numpy as np
import pandas as pd

def split_memory_string(input_string):
    """Splits the strings in the following way:
    input_string: '256GB SSD + 256GB SSD'
    returns '256GB SSD', '256GB SSD'
    """
    plus_index = input_string.find('+')
    if plus_index == -1:
        return input_string.strip(), ''
    str1 = input_string[:plus_index].strip()
    str2 = input_string[plus_index + 1:].strip()
    return str1, str2


def take_memory_and_type_from_one(word_in):
    """Extracts data about the memory from 
    the string of the form eg '128GB SSD' 
    (the one from the Memory column) into:
    [size(float), 'type'],
    where 
        size is in GB 
        type can have values: 'SSD', 'HDD', 'other'
    """
    match = re.search(r'(\d+)(GB|TB) (SSD|HDD|.*)', word_in)
    if match:
        size = float(match.group(1))
        size = size if match.group(2) == 'GB' else size * 1024  # Convert TB to GB
        type = match.group(3)
        return [size, type]
    return [0, 'Other']


def take_size_type_fromMemory(word_in):
    """When a word of the format '256GB SSD + 256GB SSD' 
    is given it returns a list of the format:
    [size (float), 'type', size (float), 'type']
    """
    if '+' in word_in:
        words = split_memory_string(word_in)
        result = take_memory_and_type_from_one(words[0]) + take_memory_and_type_from_one(words[1])
        return result
    return take_memory_and_type_from_one(word_in)


def extract_numeric(value):
    """Extracts numeric value from a given word
    eg '1.2GHz' (string) -> 1.2 (float)
    """
    match = re.search(r'\d+(\.\d+)?', value)
    return float(match.group()) if match else None


def take_Ghz_fromCPU(data):
    """Extracts number of GHz from a typical 
    value in the 'Cpu' column.
    """
    words = data.split()
    word = words[-1]
    if 'GHz' in word:
        return extract_numeric(word)
    raise ValueError("The last word is not of the form '2.3GHz'!")


def take_nrofPixels_fromScreenResolution(data):
    """Extracts number of pixels from the 'ScreenResolution' column
    eg: 'Full HD 1920x1080' (string) -> 2073600 (float)
    """
    resolution = data.split()[-1]
    width, height = map(int, resolution.split('x'))
    return float(width * height)


def str_to_num_extractor(data, col_ix):
    """Applies extract_numeric to an entire column."""
    data[col_ix] = data[col_ix].apply(extract_numeric)
    return data


def memory_extractor(memory_column):
    """Extracts information from the 'Memory' column."""
    total_memory, SSD, HDD, Other = np.zeros((4, memory_column.size))
    
    for i, mem in enumerate(memory_column):
        memory_info = take_size_type_fromMemory(mem)
        total_memory[i] = sum(memory_info[::2])
        SSD[i] = 1 if 'SSD' in mem else 0
        HDD[i] = 1 if 'HDD' in mem else 0
        Other[i] = 1 if SSD[i] == 0 and HDD[i] == 0 else 0
    
    return [{"MemorySize": total_memory},{ "SSD": SSD}, {"HDD": HDD}, {"Other": Other}]


def cpu_extractor(cpu_column):
    """Extracts information from the 'Cpu' column."""
    return {"cpu_GHz": np.array([take_Ghz_fromCPU(cpu) for cpu in cpu_column])}


def screenResolution_extractor(screenResolution_column):
    """Extracts information from the 'ScreenResolution' column."""
    return {"nr_pixels": np.array([take_nrofPixels_fromScreenResolution(res) for res in screenResolution_column])}


def Gpu_company_extractor(Gpu_column):
    """Extracts information from the 'Gpu' column."""
    companies = ['Intel', 'AMD', 'Nvidia']
    data_dict = {company: np.zeros(Gpu_column.size) for company in companies}
    data_dict['Other_GPU_company'] = np.zeros(Gpu_column.size)
    
    for i, gpu in enumerate(Gpu_column):
        found = False
        for company in companies:
            if company in gpu:
                data_dict[company][i] = 1
                found = True
                break
        if not found:
            data_dict['Other_GPU_company'][i] = 1
    
    return data_dict


def ScreenResolution_touchscreen_extractor(screenResolution_column):
    """Extracts information from the 'ScreenResolution' column about touchscreen."""
    return {'touchscreen': np.array([1 if 'Touchscreen' in res else 0 for res in screenResolution_column])}
