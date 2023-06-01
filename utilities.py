import pandas as pd

def import_dat_return_data(path_to_dat_file:str):
    """
        Imports existing .dat file from LabView Software and fit data in pd.Dataframe.
        Parameters
        ----------
        path_to_dat_file : string
            Path to .dat file.
        Returns
        -------
        data_2 : pd.Dataframe
            contains voltage values of the electrodes to timestamp
        meta : list
            contains meta information about imported file
        names_formatted_list : list
            contains formatted column headers for pd.dataframe
        error_val : string
            contains error notice of width of the data
    """
    import pandas as pd
    import fnmatch
    #Read meta data and format it into a list
    i = pd.read_csv(path_to_dat_file , sep="\s+", encoding="cp1252", nrows=0)
    meta = list(i.columns.values)
    #Read time and amplitude data for checking
    data = pd.read_csv(path_to_dat_file, sep="\s+", encoding="cp1252", skiprows=3, nrows=6)
    #Read names of electrodes and format into list
    names_unformatted = pd.read_csv(path_to_dat_file, sep="\t", encoding="cp1252", skiprows=[0,1], nrows=1)
    names_unformatted_list = list(names_unformatted.columns.values)
    names_formatted_list=[]
    my_pattern = "Unnamed:*"
    for name_to_check in names_unformatted_list:
        if not fnmatch.fnmatch(name_to_check, my_pattern):
            j = name_to_check.replace(' ','')
            names_formatted_list.append(j)
    #Check if length of names and length of data is equal
    len_of_names_formatted_list = len(names_formatted_list)
    len_of_data = len(data.columns)
    error_var = "Length of names fits length of data"
    if len_of_names_formatted_list != len_of_data:
        error_var = "Length of names doesn't fit length of data: " + str(len_of_names_formatted_list) + " != " + str(len_of_data)
    #Read time and amplitude data. Fitting formatted names into data and remove units
    data_2 = pd.read_csv(path_to_dat_file, sep="\s+", encoding="cp1252", names = names_formatted_list, skiprows=4)
    rec_dur = data_2.iloc[:, 0].max() # Recording Duration
    meta.append(rec_dur)
    #Return values
    print(".dat file successfully imported and into pd.dataframe formatted")
    return data_2, meta, names_formatted_list, error_var

def series_to_string(series:pd.Series, verbose=False):
    """
        Modifies the series of a pd.DataFrame into a string, which can be imported by Matlab-based DrCell Software
        Parameters
        ----------
        series : pd.Series
            Input series with \n as separator
        verbose: bool
            Default False. True prints current series
        Returns
        -------
        return_string : string
            Returns modified string with two beginning blanks, tabstop as separator and custom blanks between values
    """
    import pandas as pd

    if verbose == True:
        print(series)

    y = series.to_string(header=False, index=False)
    y1 = y.replace(' ','')
    y2 = y1.replace('\n-','\t -')
    y3 = y2.replace('\n', '\t  ')
    blanks = '  '
    y4 = blanks+y3
    return_string = y4

    if verbose == True:
        print(return_string)

    return return_string

def append_row_to_dat(row_to_be_written:str, path:str, encoding:str='cp1252'):
    """
        Appends row to existing .dat file, which can be imported by Matlab-based DrCell Software.
        If no .dat file exists it gets generated.
        Parameters
        ----------
        row_to_be_written : string
            String which contains a row for a .dat file.
        path : string
            Path to .dat file.
        encoding : string, optional
            The encoding in which the .dat file is saved.
            Default: cp1252
        Returns
        -------
        None
    """
    with open(path, 'a', encoding=encoding) as file:
        file.write(row_to_be_written + '\n')
    return None

