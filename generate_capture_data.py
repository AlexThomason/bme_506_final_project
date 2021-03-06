# generate_capture_data.py
# Author: Alex Thomason


# Import necessary packages
import numpy as np


def find_nearest(a, a0):
    """
    Finds the element (and its index) in nd array `a` closest to the scalar
    value `a0`
    Args:
        a (np.array or list): array of values
        a0 (int or float): value to find in np array 'a'
    Returns:
        idx (int): index of the element in nd array `a` closest to the scalar
                   value `a0`
        nearest_val (int or float): element in nd array `a` closest to the
                                    scalar value `a0`
    """
    a = np.asarray(a)
    idx = np.abs(a - a0).argmin()
    idx = int(idx)
    nearest_val = a[idx]
    return idx, nearest_val


def generate_capture_data(filename: str, duration: int or float,
                          capture_voltage: int):
    """
    This function creates a file and generates data

    The data generated has the following columns:
        (1) stimulus duration - constant pulse duration
        (2) Stimulus Voltage Amplitude - varying voltage of the stimulus
        (3) Capture Status (1 = capture, 0 = no capture)

    Args:
        filename (str): name of test data file to be created
        duration (int or float): pulse duration
        capture_voltage(): min stimulation voltage that
                           captures myocardial tissue at
                           the provided pulse duration

    Returns:
        file with 3 columns of data described above
    """
    data_length = 500      # length of data
    stim_duration = duration * np.ones((data_length))
    stim_voltage = np.arange(0, 5, 5/data_length)
    capture_status = np.zeros((data_length))
    index, _ = find_nearest(stim_voltage, capture_voltage)
    capture_status[index:] = 1
    data = np.column_stack([stim_duration, stim_voltage, capture_status])
    np.savetxt(filename, data, fmt=['%.2f', '%.2f', '%d'], delimiter=',')


# Generate psuedo data for the energy saving algorithm
def create_patient_capture_data_files(pulse_duration_experimental: list,
                                      voltage_amp_experimental: list,
                                      patient_name: str):
    """This function creates capture data files and generates data
    for a given patient.

    This function takes in a list of experimental pulse duration
    and voltage amplitudes for a given patient and creates
    psuedo experimental data for the energy saving algorithm.

    Args:
        pulse_duration_experimental (list): list of floats containing
                    experimental pulse durations. List must be the same
                    length as voltage_amp_experimental
        voltage_amp_experimental (list): list of floats containing
                    experimental voltage amplitudes that capture
                    the myocardial tisuee of the patient. List must
                    be the same length as pulse_duration_experimental
        patient_name: name of the patient that the data belongs to

    Returns:
        Several files (same number of files as there are objects in
        the input lists) containing data as described in the
        generate_capture_data() function
    """
    for duration_val, voltage_val in zip(pulse_duration_experimental,
                                         voltage_amp_experimental):
        generate_capture_data("test_data/{}_{}ms.csv".format(patient_name,
                              duration_val), duration_val, voltage_val)


if __name__ == "__main__":
    # Sample Strength-duration data
    # https://d1wqtxts1xzle7.cloudfront.net/50956640/j.1540-8159.2009.02456.x2x0161218-19709-1lbuxg3-with-cover-page-v2.pdf?Expires=1635175866&Signature=N-ROBbokpqOa-5ioS8HXjMkeKh2I7sGkPqwLSjghrTBY7wRHJ75ELUi2FyERHH3acmAdyosEmHjI14bsrWXjqBZfxheNTCjoXw8qNEmJFiRXeWNbcy4kvfvMrdIDYqUcCFME-~beHZc51a4AazX4JsYplcBhMsVn9ljTvyy-tW4x21UFg31FaQzLI~yt2mevWPPXGYqpeoK62G7PesuSft~r-6g-HHU6DoBxXOH8rO01y0N5EZ2TT7yVx8xIrDASKRl4t~VQryRaK6kMWrgJ5EEmJTZDWHXnBI3aB7HS3PyHpnHZigCs8MiLGMJm7P0IMf5NV9XTUOXFbCBf7E1Zww__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA

    # ____PATIENT 1____
    # Pulse duration [ms] of patient 1
    duration_experimental = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.4]
    # Voltage amplitude [V] of patient 1
    voltage_experimental = [5, 3.5, 2.8, 2.6, 2.4, 2.2, 2.2]
    create_patient_capture_data_files(duration_experimental,
                                      voltage_experimental, "patient1")

    # ____PATIENT 2____
    # Pulse duration [ms] of patient 2
    duration_experimental = [0.3, 0.5, 0.8, 1, 1.5]
    # Voltage amplitude [V] of patient 2
    voltage_experimental = [2.25, 1.55, 1.25, 1.15, 0.92]
    create_patient_capture_data_files(duration_experimental,
                                      voltage_experimental, "patient2")
