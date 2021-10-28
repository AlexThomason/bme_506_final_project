# generate_capture_data.py
# Author: Alex Thomason


# Import necessary packages
import numpy as np
import logging


def find_nearest(a, a0):
    """
    Finds the element (and its index) in nd array `a` closest to the scalar
    value `a0`
    Args:
        a (np.array): array of values
        a0 (int or float): value to find in np array 'a'
    Returns:
        idx (int): index of the element in nd array `a` closest to the scalar
                   value `a0`
        nearest_val (int or float): element in nd array `a` closest to the
                                    scalar value `a0`
    """
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
        filename (str): name of test data file
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
    np.savetxt(filename, data, fmt=['%.2f', '%.2f', '%d'], delimiter='\t')


# Generate psuedo data for the energy saving algorithm
def create_capture_data_file(pulse_duration_experimental,
                             voltage_amp_experimental,
                             patient_name):
    for duration_val, voltage_val in zip(pulse_duration_experimental,
                                         voltage_amp_experimental):
        generate_capture_data("{}_{}ms".format(patient_name, duration_val),
                              duration_val, voltage_val)


if __name__ == "__main__":
    # Sample Strength-duration data
    # https://d1wqtxts1xzle7.cloudfront.net/50956640/j.1540-8159.2009.02456.x2x0161218-19709-1lbuxg3-with-cover-page-v2.pdf?Expires=1635175866&Signature=N-ROBbokpqOa-5ioS8HXjMkeKh2I7sGkPqwLSjghrTBY7wRHJ75ELUi2FyERHH3acmAdyosEmHjI14bsrWXjqBZfxheNTCjoXw8qNEmJFiRXeWNbcy4kvfvMrdIDYqUcCFME-~beHZc51a4AazX4JsYplcBhMsVn9ljTvyy-tW4x21UFg31FaQzLI~yt2mevWPPXGYqpeoK62G7PesuSft~r-6g-HHU6DoBxXOH8rO01y0N5EZ2TT7yVx8xIrDASKRl4t~VQryRaK6kMWrgJ5EEmJTZDWHXnBI3aB7HS3PyHpnHZigCs8MiLGMJm7P0IMf5NV9XTUOXFbCBf7E1Zww__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA

    # patient 1
    duration_experimental = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.4]
    voltage_experimental = [5, 3.5, 2.8, 2.6, 2.4, 2.2, 2.2]
    create_capture_data_file(duration_experimental,
                             voltage_experimental, "patient1")
