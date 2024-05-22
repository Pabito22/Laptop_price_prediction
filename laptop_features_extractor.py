def split_memory_string(input_string):
    """Splits the strings in the following way:
    input_string: '256GB SSD +  256GB SSD'
    returns '256GB SSD ', '256GB SSD'
    """
    # Find the position of the plus sign
    plus_index = input_string.find('+')
    
    # Split the string into two parts
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
        type can have values: 'SSD', 'HDD', 'other
    """
    word = ''
    j = 0
    for i in word_in:
        if i.isdigit(): #check if a number
            word = word + i
            #check the size of memory
            if(word_in[j+1]=='G'):
                number = float(word) #for GB
            else:
                number = float(word)*1024 #for TB
        j=j+1
        
    #check what type of memory and return
    if 'SSD' in word_in:
        return [number, 'SSD']
    elif 'HDD' in word_in:
        return [number, 'HDD']
    else:
        return [number, 'Other']



def take_memory_size_and_type(word_in):
    """
    when a word of the format '256GB SSD +  256GB SSD'
    is given it returns a list of the format:
    [size (float), 'type', size (float), 'type']
    where size is in GB 
        type can have values 'SSD', 'HDD', 'other
    Parameters:
    input_string: a string from the Memory column
    """
    if '+' in word_in:
        words = split_memory_string(word_in)
        wynik = take_memory_and_type_from_one(words[0])
        wynik.append(take_memory_and_type_from_one(words[1])[0])
        wynik.append(take_memory_and_type_from_one(words[1])[1])
        return wynik
    else:
        return take_memory_and_type_from_one(word_in)


    
