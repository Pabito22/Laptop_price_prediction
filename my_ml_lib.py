import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

def num_attrs_combinations(DataFrame_num_o):
    """
    Create a new DataFrame containing combinations of existing numerical attributes as ratios,
    and include the label column from the original DataFrame.

    For each pair of numerical attributes in the input DataFrame (excluding the last column, assumed to be the label),
    the function generates two new attributes representing the ratio of each attribute to the other. If division by zero
    occurs, it skips that particular combination.

    Parameters:
    - DataFrame_num_o (pandas.DataFrame): The input DataFrame containing numerical attributes and a label column as the last column.

    Returns:
    - new_df (pandas.DataFrame): A new DataFrame containing the generated ratio attributes (without the label!).

    Example:
    >>> import pandas as pd
    >>> data = {
    >>>     'Feature1': [1, 2, 3, 4, 5],
    >>>     'Feature2': [5, 4, 3, 2, 1],
    >>>     'Label': [10, 20, 30, 40, 50]
    >>> }
    >>> df = pd.DataFrame(data)
    >>> new_df = num_attrs_combinations(df)
    >>> print(new_df)
       Feature1_per_Feature2  Feature2_per_Feature1  
    0                   0.20                   5.00     
    1                   0.50                   2.00     
    2                   1.00                   1.00     
    3                   2.00                   0.50     
    4                   5.00                   0.20     
    """
    DataFrame_num = DataFrame_num_o.copy()
    new_df = pd.DataFrame()
    attrs_size = DataFrame_num.columns.size - 1 # don't count the label

    for i in range(attrs_size):
        for j in range(i + 1, attrs_size):
            col_i = DataFrame_num.columns[i]
            col_j = DataFrame_num.columns[j]
            try:
                new_attr_val = DataFrame_num.iloc[:, i] / DataFrame_num.iloc[:, j]
                new_attr_name = col_i + "_per_" + col_j
                new_df[new_attr_name] = new_attr_val
            except ZeroDivisionError:
                try:
                    new_attr_val = DataFrame_num.iloc[:, j] / DataFrame_num.iloc[:, i]
                    new_attr_name = col_j + "_per_" + col_i
                    new_df[new_attr_name] = new_attr_val
                except ZeroDivisionError:
                    continue
    
    # assign the label to the new Data Frame
    label_column = DataFrame_num.columns[-1]
    new_df[label_column] = DataFrame_num[label_column].values
    
    return new_df.drop(columns=[label_column]) #remove the label
        


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
    - potential_attrs (pandas.Index): A pandas Index containing the names of attributes that meet the criteria.
    - corrs_with_label (numpy.ndarray): An array containing the correlation coefficients of the attributes
      with respect to the label.

    """
    corr_matrix = DataFr.corr()
    attrs_corrs = corr_matrix[label_name].drop(label_name).values
    potential = np.logical_or(attrs_corrs > corr_tresh, attrs_corrs < -corr_tresh)
    potential_attrs = corr_matrix[label_name].drop(label_name).index[potential]

    return potential_attrs, attrs_corrs[potential]


