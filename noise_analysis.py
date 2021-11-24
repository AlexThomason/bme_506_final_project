# energy_saver_algorthm.py
# Author: Alex Thomason


# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import generate_capture_data as gcd
import strength_duration_curve as sdc
import capture_threshold_detection as ctd
import os


def add_random_noise_to_data(orig_data: list, sd: float):
    """Adds random noise to data

    Args:
        orig_data (list): list of original data points
        sd (float): standard deviation of noise

    Returns:
        noisy_data (list): list of noisy data
    """
    # Generate noise
    np_orig_data = np.array(orig_data)
    shape = np_orig_data.shape
    noise_mean = 0
    noise = np.random.normal(noise_mean, sd, shape)
    noisy_data = orig_data + noise
    return noisy_data


def add_predictable_noise_to_data(orig_data: list, noise_voltage: float):
    """Adds predictable noise to data

    Args:
        orig_data (list): list of original data points
        voltage noise (float): voltage noise to add to the data

    Returns:
        noisy_data (list): list of noisy data
    """
    # Generate noise
    np_orig_data = np.array(orig_data)
    noisy_data = np_orig_data + noise_voltage
    return noisy_data


def patient_file_list(patient_name: str):
    """ Finds the data files for a patient and
    returns the filenames in a list of strings

    Finds patient files within the "test_data" directory

    Args:
        patinet_name (str): name of the patient whos data files
                            you want to be returned in a list

    Returns:
        filename_list (list): list of strings of the filenames of
                              a given patient
    """
    filename_list = []
    path = "test_data"
    for file in os.listdir(path):
        if file.startswith(patient_name):
            filename_list.append(file)
    return filename_list


def delete_patient_files(patient_name: str):
    """Deletes data files of a specified patient

    Deletes patient files within the "test_data" directory

    Args:
        patinet_name (str): name of the patient whos data files
                            you want to delete
    Returns:
        none
    """
    path = "test_data"
    for file in os.listdir(path):
        if file.startswith(patient_name):
            os.remove(path + "/" + file)


def noise_study(duration_experimental, voltage_experimental,
                noise_voltage_list):
    """This function does the following:

    (1) Finds rheobase and chronaxie of the original simulus
        amplitude vs duration data
    (2) Iterates over the input noise amplitude vector
    (3) Adds noise to the original simulus amplitude data
    (4) Creates capture data files for the noisy stimulus voltage data
    (5) Uses the capture_threshold_algorithm to find the capture voltages
    (6) Finds the chronaxie and rheobase for the noisy capture voltages
        found by the capture_threshold_algorithm
    (7) Finds the percent difference between the rheobase and chronaxie
        of the original data and the the noisy data

    Args:
        duration_experimental (list): stimulus duration values [ms]
        voltage_experimental (list):  stimulus amplitude values [V]
        noise_voltage_list (list): Noise voltage amplitude. Each item
            in the list is a the amplitude of noise that is added to
            an the entire voltage_experimental list.

    Returns:
        Plot of percent difference of chronaxie or rheobase vs the amount
        of amplitude added to the voltage_experimental list
    """
    rheobase_list = []
    chronaxie_list = []
    perc_diff_list_rheobase = []
    perc_diff_list_chronaxie = []

    # Finds rheobase and chronaxie of the original simulus
    # amplitude vs duration data
    rheobase_orig, chronaxie_orig, min_pulse_energy = \
        sdc.patient_data_manipulation(duration_experimental,
                                      voltage_experimental)

    # Adds noise to the original simulus amplitude data
    # Creates capture data files for the noisy stimulus voltage data
    for noise in noise_voltage_list:
        noisy_voltage_experimental = add_predictable_noise_to_data(
            voltage_experimental, noise)
        patient_name = "noise_test_patient"
        gcd.create_patient_capture_data_files(duration_experimental,
                                              noisy_voltage_experimental,
                                              patient_name)

        filename_list = patient_file_list(patient_name)

        capture_duration_data = []
        capture_voltage_data = []

        # Uses the capture_threshold_algorithm to find the capture voltages
        for filename in filename_list:
            capture_duration, capture_voltage = \
                    ctd.find_patient_capture_voltage(filename)
            capture_duration_data.append(capture_duration)
            capture_voltage_data.append(capture_voltage)

        # Deletes the recently created capture data files for the
        # noisy stimulus voltage data
        delete_patient_files(patient_name)

        # Finds the chronaxie and rheobase for the noisy capture voltages
        # found by the capture_threshold_algorithm
        rheobase_noise, chronaxie_noise = sdc.strength_duration_trend_line(
            capture_duration_data, capture_voltage_data)

        rheobase_list.append(rheobase_noise)
        chronaxie_list.append(chronaxie_noise)

        perc_diff_rheobase = sdc.percent_difference([rheobase_orig],
                                                    [rheobase_noise])
        perc_diff_list_rheobase.append(perc_diff_rheobase)

        perc_diff_chronaxie = sdc.percent_difference([chronaxie_orig],
                                                     [chronaxie_noise])
        perc_diff_list_chronaxie.append(perc_diff_chronaxie)

    print(rheobase_list)
    print(chronaxie_list)
    print(perc_diff_list_rheobase)
    print(perc_diff_list_chronaxie)

    plt.plot(noise_voltage_list, perc_diff_list_rheobase,
             '-*', label="% Difference Rheobase")
    plt.plot(noise_voltage_list, perc_diff_list_chronaxie, '-*',
             label="% Difference Chronaxie")
    plt.xlabel('Volts [v] Added to Capture Threshold Data')
    plt.ylabel('% Difference')
    plt.title("% Difference of Rheobase & Chronaxie From Added Noise Voltage")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    duration_experimental = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.4]
    voltage_experimental = [5, 3.5, 2.8, 2.6, 2.4, 2.2, 2.2]
    noise_voltage_list = np.arange(0, 0.20, 0.01)

    noise_study(duration_experimental, voltage_experimental,
                noise_voltage_list)
