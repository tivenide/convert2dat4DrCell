#
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

def convert_insilico_generated_mea_datafile_to_dr_cell_dat(source_path_csv:str, target_path_dat:str):
    """
        Converts existing .csv file from Matlab based insilico MEA generator (https://github.com/tivenide/InsilicoMEAgenerator_based_on_Lieb) to .dat file,
        which can be imported by Matlab-based DrCell Software.
        Parameters
        ----------
        source_path_csv : string
            Path to insilico generated .csv file.
        target_path_dat : string
            Path to target .dat file for DrCell Software.
        Returns
        -------
        None
    """
    import pandas as pd

    print('Conversion started')

    # reading csv
    i = pd.read_csv(source_path_csv, sep=";", encoding="cp1252", nrows=0)
    meta = list(i.columns.values)
    df = pd.read_csv(source_path_csv, sep=";", encoding="cp1252", skiprows=2)
    print('Reading .csv finished, starting .dat creation ...')

    # converting time units from [s] to [ms] and round values
    df.iloc[:,0] = df.iloc[:,0] * 1000
    df = df.round(2)

    # data for header
    first_line = ''
    meta_string = meta[0] + ', ' + meta[1] + ', ' + meta[2] + ' ' + meta[3] + ', ' + meta[4]
    electrode_string = ' t	El 21	El 31	El 41	El 51	El 61	El 71	El 12	El 22	El 32	El 42	El 52	El 62	El 72	El 82	El 13	El 23	El 33	El 43	El 53	El 63	El 73	El 83	El 14	El 24	El 34	El 44	El 54	El 64	El 74	El 84	El 15	El 25	El 35	El 45	El 55	El 65	El 75	El 85	El 16	El 26	El 36	El 46	El 56	El 66	El 76	El 86	El 17	El 27	El 37	El 47	El 57	El 67	El 77	El 87	El 28	El 38	El 48	El 58	El 68	El 78'
    units_string = '[ms] [µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]'
    footer_string = ''

    # building header
    append_row_to_dat(first_line, target_path_dat)
    append_row_to_dat(meta_string, target_path_dat)
    append_row_to_dat(electrode_string, target_path_dat)
    append_row_to_dat(units_string, target_path_dat)

    # building data rows
    for index, row in df.iterrows():
        string = series_to_string(row)
        append_row_to_dat(string, target_path_dat)

    #append_row_to_dat(footer_string, target_path_dat)

    print('Conversion successfully finished')

    return None

def convert_dr_cell_dat_to_dr_cell_dat(source_path_csv:str, target_path_dat:str):
    """
        Converts existing .dat file from LabView Software to .dat file,
        which can be imported by Matlab-based DrCell Software. Just for testing reasons.
        Parameters
        ----------
        source_path_csv : string
            Path to .dat file.
        target_path_dat : string
            Path to target .dat file for DrCell Software.
        Returns
        -------
        None
    """
    import pandas as pd

    print('Conversion started')

    # reading csv
    df, meta, names_formatted_list, error_var = import_dat_return_data(source_path_csv)
    #i = pd.read_csv(source_path_csv, sep=";", encoding="cp1252", nrows=0)
    #meta = list(i.columns.values)
    #df = pd.read_csv(source_path_csv, sep=";", encoding="cp1252", skiprows=2)
    print('Reading .dat finished, starting .dat creation ...')

    # converting time units from [s] to [ms] and round values
    #df.iloc[:,0] = df.iloc[:,0] * 1000
    #df = df.round(2)

    # data for header
    first_line = ''
    meta_string = meta[0] + ' ' + meta[1] + ' ' + meta[2] + ' ' + meta[3] + ' ' + meta[4]
    electrode_string = ' t	El 21	El 31	El 41	El 51	El 61	El 71	El 12	El 22	El 32	El 42	El 52	El 62	El 72	El 82	El 13	El 23	El 33	El 43	El 53	El 63	El 73	El 83	El 14	El 24	El 34	El 44	El 54	El 64	El 74	El 84	El 15	El 25	El 35	El 45	El 55	El 65	El 75	El 85	El 16	El 26	El 36	El 46	El 56	El 66	El 76	El 86	El 17	El 27	El 37	El 47	El 57	El 67	El 77	El 87	El 28	El 38	El 48	El 58	El 68	El 78'
    units_string = '[ms] [µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]	[µV]'
    footer_string = ''

    # building header
    append_row_to_dat(first_line, target_path_dat)
    append_row_to_dat(meta_string, target_path_dat)
    append_row_to_dat(electrode_string, target_path_dat)
    append_row_to_dat(units_string, target_path_dat)

    # building data rows
    for index, row in df.iterrows():
        string = series_to_string(row)
        append_row_to_dat(string, target_path_dat)

    #append_row_to_dat(footer_string, target_path_dat)

    print('Conversion successfully finished')

    return None


if __name__ == '__main__':

    source_path_csv= r'data_origin.dat'
    target_path_dat= r'data.dat'

    #convert_insilico_generated_mea_datafile_to_dr_cell_dat(source_path_csv, target_path_dat)
    convert_dr_cell_dat_to_dr_cell_dat(source_path_csv, target_path_dat)

    print('main finished')
