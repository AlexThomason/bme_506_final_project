# energy_saver_algorthm.py
# Author: Alex Thomason


# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as so
import scipy.interpolate as si
import logging

from scipy.sparse.extract import find


# Sample Strength-duration data
# https://d1wqtxts1xzle7.cloudfront.net/50956640/j.1540-8159.2009.02456.x20161218-19709-1lbuxg3-with-cover-page-v2.pdf?Expires=1635175866&Signature=N-ROBbokpqOa-5ioS8HXjMkeKh2I7sGkPqwLSjghrTBY7wRHJ75ELUi2FyERHH3acmAdyosEmHjI14bsrWXjqBZfxheNTCjoXw8qNEmJFiRXeWNbcy4kvfvMrdIDYqUcCFME-~beHZc51a4AazX4JsYplcBhMsVn9ljTvyy-tW4x21UFg31FaQzLI~yt2mevWPPXGYqpeoK62G7PesuSft~r-6g-HHU6DoBxXOH8rO01y0N5EZ2TT7yVx8xIrDASKRl4t~VQryRaK6kMWrgJ5EEmJTZDWHXnBI3aB7HS3PyHpnHZigCs8MiLGMJm7P0IMf5NV9XTUOXFbCBf7E1Zww__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA



# Begin Modular Function Code
"""def find_power_trend_line(x_data, y_data):
    popt, pcov = so.curve_fit(lambda fx,a,b: a*fx**-b,  x_data,  y_data, method="lm")
    x = np.arange(0, 2, 0.1)
    power_y = popt[0]*x**-popt[1]
    plt.scatter(x_data, y_data, label='actual data')
    plt.plot(x, power_y, label='power-fit')
    plt.legend()
    plt.show()
    print("optimal equation is: y = {} * x^(-{})".format(popt[0],popt[1]))
    return popt"""

def interpolate_data_points(x_data, y_data):
    """
    Interpolates data

    Args:
        x_data (list or np.array): x values
        y_data (list or np.array): y values to be interpolated

    Returns:
        x_new (np.array): new array of x values
        y_new (np.array): interpolated array of y values
    """
    f = si.interp1d(x_data, y_data)
    x_new = np.arange(x_data[0], x_data[-1], 0.01)
    y_new = f(x_new)
    plt.plot(x_data, y_data, 'o', label="Experimental Data")
    plt.plot(x_new, y_new, '-', label="Interpolated Data")
    plt.xlabel('Pulse Duration [ms]')
    plt.ylabel('Voltage Amplitude [ms]')
    plt.legend()
    plt.show()
    return x_new, y_new


def find_nearest(a, a0):
    """
    Finds the element (and its index) in nd array `a` closest to the scalar value `a0`

    Args:
        a (np.array): array of values
        a0 (int or float): value to find in np array 'a'

    Returns:
        idx (int): index of the element in nd array `a` closest to the scalar value `a0`
        nearest_val (int or float): element in nd array `a` closest to the scalar value `a0`
    """
    idx = np.abs(a - a0).argmin()
    idx = int(idx)
    nearest_val = a[idx]
    return idx, nearest_val


def find_capture_voltage(duration_val: int or float, duration_data, voltage_amp_data):
    """
    Finds the minimum voltage it takes to capture mycardial tissue. In other words, this function
    finds the voltage amplitude for a pulse duration

    Args:
        duration_val (int or float): pulse duration value
        duration_data (list or array): interpolated pulse duration data
        voltage_amp_data (list or array): interpolated voltage amplitude data

    Returns:
        capture_voltage (int or float): voltage amplitude to caputre the myocardial tissue
    """
    index, nearest_duration = find_nearest(duration_data, duration_val)
    capture_voltage = voltage_amp_data[index]
    capture_voltage = round(capture_voltage, 2)
    print("The duration value you entered is: {} ms".format(duration_val))
    print("The nearest duration value to the one you entered is: {} ms".format(round(nearest_duration,3)))
    print("The capture voltage is {} V at a duration of {} ms".format(capture_voltage, round(nearest_duration,3)))
    return capture_voltage


def find_rheobase_chronaxie(duration_data, voltage_amp_data):
    """
    Calculates Rheobase and Chronaxie. The pulse duration and voltage amplitude data
    should be interpolated data to get the most accurate results.

    Args:
        duration_data (list or array): interpolated pulse duration data
        voltage_amp_data (list or array): interpolated voltage amplitude data

    Returns:
        rheobase (float): Rheobase =  the minimal electric current required to excite a tissue
        chronaxie (float): chronaxie = minimum time required for an electric current double
                           the strength of the rheobase to stimulate a tissue
    """
    # Calculate Rheobase
    rheobase = voltage_amp_data[-1]
    rheobase = round(rheobase, 3)
    print("Rheobase = {} V".format(rheobase))
    # Calculate Chronaxie
    index, double_rheobase = find_nearest(voltage_amp_data, 2*rheobase)
    print("Double Rheobase = {} V".format(double_rheobase))
    chronaxie = duration_data[index]
    chronaxie = round(chronaxie, 3)
    print("Chronaxie = {} ms".format(chronaxie))
    return rheobase, chronaxie


def generate_capture_data(filename: str, duration: int, capture_voltage: int):
    """
    This function creates a file and generates data

    The data generated has the following columns:
            (1) stimulus duration, (2) Stimulus Voltage Amplitude,
            (3) Capture Status (1 = capture, 0 = no capture)

    """
    data_length = 500      # length of data
    stim_duration = duration * np.ones((data_length))
    stim_voltage = np.arange(0, 5, 5/data_length)
    capture_status = np.zeros((data_length))
    index = np.where(stim_voltage==capture_voltage)
    index = index[0][0]
    capture_status[index:] = 1
    data = np.column_stack([stim_duration, stim_voltage, capture_status])
    np.savetxt(filename , data, fmt=['%.2f','%.2f','%d'], delimiter='\t')


def main_patient_1():
    """
    This function takes in experimental data and returns
    """
    pulse_duration = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.4]    # [ms] Pulse duration of patient 1
    voltage_amp = [5, 3.5, 2.8, 2.6, 2.4, 2.2, 2.2]   # [V] Voltage amplitude of patient 1
    interp_pulse_duration, interp_voltage_amp = interpolate_data_points(pulse_duration,
                                                                        voltage_amp)
    duration_val_1 = 0.8    # [ms] Duration Value
    capture_voltage = find_capture_voltage(duration_val_1,interp_pulse_duration,
                                           interp_voltage_amp)
    rheobase, chronaxie = find_rheobase_chronaxie(interp_pulse_duration,
                                                  interp_voltage_amp)


if __name__ == "__main__":
    main_patient_1()

duration = 0.8
capture_voltage = 2.5
data_length = 500      # length of data
stim_duration = duration * np.ones((data_length))
print(stim_duration)
stim_voltage = np.arange(0, 5, 5/data_length)
print(stim_voltage)
capture_status = np.zeros((data_length))
print(capture_status)
print(len(capture_status))
index = np.where(stim_voltage==capture_voltage)
index = index[0][0]
print(index)
capture_status[index:] = 1
print(capture_status)

generate_capture_data("test_data", duration=0.8, capture_voltage=3)