def convert_MEArec_insilico_generated_60mea_datafile_to_dr_cell_dat(source_path_h5:str, target_path_dat:str):
    """
        Converts existing .h5 file from python based insilico MEA generator MEArec (https://github.com/alejoe91/MEArec) to .dat file,
        which can be imported by Matlab-based DrCell Software.
        Parameters
        ----------
        source_path_h5 : string
            Path to insilico generated .h5 file.
        target_path_dat : string
            Path to target .dat file for DrCell Software.
        Returns
        -------
        None
    """
    import pandas as pd
    import h5py  # hdf5
    import numpy as np

    from main import append_row_to_dat, series_to_string

    print('Conversion started')
    h5 = h5py.File(source_path_h5, 'r')
    signal_raw = np.array(h5["recordings"])
    timestamps = np.array(h5["timestamps"])

    # hardcoding meta data
    Date = '16.06.2023'
    Time = '10:50:27'
    fs = '10000'
    meta = [Date, Time, fs, "Hz", "Raw"]


    # Reorder the columns
    column_order = [   13, 21, 29, 37, 45, 53,
                    5, 12, 20, 28, 36, 44, 52, 59,
                    4, 11, 19, 27, 35, 43, 51, 58,
                    3, 10, 18, 26, 34, 42, 50, 57,
                    2,  9, 17, 25, 33, 41, 49, 56,
                    1,  8, 16, 24, 32, 40, 48, 55,
                    0,  7, 15, 23, 31, 39, 47, 54,
                        6, 14, 22, 30, 38, 46    ]

    #column_order = [46, 38, 30, 22, 14, 6, 54, 47, 39, 31, 23, 15, 7, 0, 55, 48, 40, 32, 24, 16, 8, 1, 56, 49, 41, 33, 25, 17, 9, 2, 57, 50, 42, 34, 26, 18, 10, 3, 58, 51, 43, 35, 27, 19, 11, 4, 59, 52, 44, 36, 28, 20, 12, 5, 53, 45, 37, 29, 21, 13]

    signal_raw_reordered = signal_raw[:, column_order]

    # stacking time and signal raw data together
    combined_data = np.hstack((timestamps.reshape(-1,1), signal_raw_reordered))
    df = pd.DataFrame(combined_data)
    print('Reading .h5 finished, starting .dat creation ...')

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