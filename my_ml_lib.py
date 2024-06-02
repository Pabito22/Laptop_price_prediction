import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

def num_attrs_combinations(DataFrame_num_o):
    """
    Returns a DataFrame with additional columns representing all possible numerical attribute combinations.

    Parameters:
    - DataFrame_num_o (pandas.DataFrame): The input DataFrame containing numerical attributes.
    !!!IT IS ASSUMED THAT THE LABEL IS IN THE LAST COLUMN OF THE DATA FRAME!!!
    Returns:
    - DataFrame_num (pandas.DataFrame): A DataFrame with additional columns representing all possible numerical attribute combinations. 
      Each combination column is named as 'Attr1_per_Attr2', where Attr1 and Attr2 are the names of the attributes involved in the combination.

    This function iterates through each pair of numerical attributes in the input DataFrame and creates new columns 
    representing their combinations (i.e., division of one attribute by another). If a division by zero occurs, 
    it tries the division in the opposite order and adds the resulting column accordingly. 
    If both attempts result in division by zero, no new column is added for that pair of attributes.

    Example:
    --------
    Suppose DataFrame_num_o is the input DataFrame:
    
        |   A   |   B   |   C   |
        |-------|-------|-------|
        |   1   |   2   |   3   |
        |   4   |   5   |   6   |
        |   7   |   8   |   9   |
    
    Calling num_attrs_combinations(DataFrame_num_o) would return a DataFrame with additional combination columns:
    
        |   A   |   B   |   C   |   A_per_B   |   A_per_C   |   B_per_C   |
        |-------|-------|-------|-------------|-------------|-------------|
        |   1   |   2   |   3   |   0.5       |   0.333...  |   0.666...  |
        |   4   |   5   |   6   |   0.8       |   0.666...  |   0.833...  |
        |   7   |   8   |   9   |   0.875...  |   0.777...  |   0.888...  |
    """
    DataFrame_num = DataFrame_num_o.copy()
    attrs_size = DataFrame_num.columns.size-1 #don't count the label
    for i in np.arange(attrs_size):
        j=i+1
        while j < attrs_size:
            try:
                new_attr_val = DataFrame_num.iloc[:,i]/DataFrame_num.iloc[:,j]
                new_attr_name = DataFrame_num.columns[i] + "_per_" + DataFrame_num.columns[j]
            except ZeroDivisionError:
                try:
                    new_attr_val = DataFrame_num.iloc[:,j] / DataFrame_num.iloc[:,i]
                    new_attr_name = DataFrame_num.columns[j] + "_per_" + DataFrame_num.columns[i]
                except ZeroDivisionError:
                    continue
            
            DataFrame_num[new_attr_name] = new_attr_val
            j+=1
    return DataFrame_num
        


def potential_attrs(DataFr, label_name, corr_tresh):
    """
    Identify attributes in a DataFrame that have a correlation coefficient greater than or less than a specified threshold
    with respect to a given label.

    Parameters:
    - DataFr (pandas.DataFrame): The DataFrame containing the dataset.
    - label_name (str): The name of the label column in the DataFrame.
    - corr_tresh (float): The threshold value for correlation coefficient. Attributes with correlation coefficients
      greater than corr_tresh or less than -corr_tresh will be considered potential attributes.

    Returns:
    - potential_attrs (pandas.Index): A pandas Index containing the names of potential attributes that meet the criteria.
    - corrs_with_label (numpy.ndarray): An array containing the correlation coefficients of the potential attributes
      with respect to the label.

    Example:
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = {'Feature1': [1, 2, 3, 4, 5], 'Feature2': [5, 4, 3, 2, 1], 'Label': [10, 20, 30, 40, 50]}
    >>> df = pd.DataFrame(data)
    >>> potential_attrs(df, 'Label', 0.5)
    (Index(['Feature2'], dtype='object'), array([-1.]))
    """
    attrs_corrs = DataFr.corr()[label_name].values

    potential = np.logical_or(attrs_corrs > corr_tresh, attrs_corrs < -corr_tresh)

    return DataFr.columns[potential], attrs_corrs[potential]

