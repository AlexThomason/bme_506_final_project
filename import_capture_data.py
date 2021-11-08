# import_capture_data.py
# Author: Alex Thomason

# Import necessary packages
import numpy as np
import logging


def import_data(filename):
    """Creates a list of each line of a file given a filename

    This function only loads files that are in the test_data directory.
    If the filename is not in the "test_data" directory (FileNotFoundError),
    then the function prints that the file does not exist in the test_data'
    directory.

    Args:
        filename (string): file name

    Returns:
        list: List containing strings of each line of the imported data
    """
    try:
        with open("test_data/" + filename, 'r') as in_file:
            in_lines = in_file.readlines()
        return in_lines
    except FileNotFoundError:
        print("The filename you entered does not exist in \
the 'test_data' directory. Please choose another file.")
        quit()


def parse_data(in_line):
    """Parses list of strings by "new line operator" and ","

    This function parses a list of strings by "new line operator" and ",".
    The output is a list of lists containing strings of the ecg data entries.

    Args:
        in_line (list): list of strings of each line of the ecg data

    Returns:
        list: List of lists containing strings of each data of the imported
              ecg data
    """
    list_split = []
    for line in in_line:
        line_strip = line.strip("\n")
        line_strip = line_strip.split(",")
        list_split.append(line_strip)
#        list_int = [float(x) for x in list_split]
    return list_split


def data_str_to_float(list_split):
    """Converts string data to float data

    This function takes a list of lists containing string values and converts
    those values to float values. If a sublist of data contains any values that
    cannot be converted into a float, the sublist is skipped and logged to the
    ecg_log.log file. If a sublist of data contains any NaN values, then that
    sublist of data is skipped and logged to the ecg_log.log file.

    Args:
        list_split (list): list of lists containing string data of the ecg data

    Returns:
        list_float: List of lists containing floats of each data of the
                    imported ecg data
    """
    import logging
    list_float = []
    for index, data_pair in enumerate(list_split):
        try:
            if "NaN" in data_pair:
                logging.info("Data entry {} with index {} contains a \
NaN value. This data pair was skipped".format(data_pair, index))
            else:
                float_data = list(map(float, data_pair))
                list_float.append(float_data)
        except ValueError:
            logging.info("Data entry {} with index {} contains a \
ValueError. Data value could not be converted into a \
float. This data pair was skipped".format(data_pair, index))
            pass
    return list_float


def isolate_data_vector(list_float, col_index):
    """Isolates a vector out of a list of lists

    This function takes list of sublists (list_float) and
    returns a vector of the values contained in the specified index
    (col_index) of each sublist.
    For example:
        IN:
        x = [[1,2],[3,4],[5,6]]\n
        vector1 = isolate_data_vector(x,0)\n
        print(vector1)

        Out:
        [1,3,5]

    Args:
        list_float: List of lists containing floats of each data of the
                    imported ecg data
        filename (string): Name of the ecg data file
    Returns:
        logging.warning: warning indicating the name of the test file
        and that voltages exceeded the normal range.
    """
    vector = []
    for data in list_float:
        vector.append(data[col_index])
    return vector


def import_parse_convert_data(filename):
    """
    This function intakes a patient file name and returns
    the column vectors as lists

    Args:
        filename (str): Name of the patient capture data

    Returns
        duration_list (list): list of floats of the duration values
        voltage_list (list): list of floats of the voltage values
        capture_list (list): list of floats of the capture status values
    """
#    logging.basicConfig(filename="log_files/{}.log".format(
#                        filename[:-4]), filemode="w",
#                        level=logging.INFO)
    patient_data_not_parsed = import_data(filename)
    patient_data_parsed = parse_data(patient_data_not_parsed)
    patient_data_float = data_str_to_float(patient_data_parsed)
    duration_list = isolate_data_vector(patient_data_float, 0)
    voltage_list = isolate_data_vector(patient_data_float, 1)
    capture_list = isolate_data_vector(patient_data_float, 2)
    return duration_list, voltage_list, capture_list


def main():
    # Patient 1
    filename = "patient1_0.1ms.csv"
    duration_list, voltage_list, capture_list = import_parse_convert_data(
                                                filename)
    return duration_list, voltage_list, capture_list


if __name__ == "__main__":
    logging.basicConfig(filename="log_files/patient1.log", filemode="w",
                        level=logging.INFO)
    duration_list, voltage_list, capture_list = main()
