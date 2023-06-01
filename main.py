
if __name__ == '__main__':

    source_path= r'data_origin.dat' # data_origin.csv , data_origin.h5
    target_path_dat= r'data.dat'

    from converter import convert_insilico_generated_mea_datafile_to_dr_cell_dat, convert_dr_cell_dat_to_dr_cell_dat, convert_MEArec_insilico_generated_60mea_datafile_to_dr_cell_dat
    #convert_insilico_generated_mea_datafile_to_dr_cell_dat(source_path, target_path_dat)
    #convert_MEArec_insilico_generated_60mea_datafile_to_dr_cell_dat(source_path, target_path_dat)
    #convert_dr_cell_dat_to_dr_cell_dat(source_path, target_path_dat)

    print('main finished')
