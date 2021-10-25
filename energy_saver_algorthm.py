# energy_saver_algorthm.py
# Author: Alex Thomason


# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as so
import logging


# Sample Strength-duration data
# https://d1wqtxts1xzle7.cloudfront.net/50956640/j.1540-8159.2009.02456.x20161218-19709-1lbuxg3-with-cover-page-v2.pdf?Expires=1635175866&Signature=N-ROBbokpqOa-5ioS8HXjMkeKh2I7sGkPqwLSjghrTBY7wRHJ75ELUi2FyERHH3acmAdyosEmHjI14bsrWXjqBZfxheNTCjoXw8qNEmJFiRXeWNbcy4kvfvMrdIDYqUcCFME-~beHZc51a4AazX4JsYplcBhMsVn9ljTvyy-tW4x21UFg31FaQzLI~yt2mevWPPXGYqpeoK62G7PesuSft~r-6g-HHU6DoBxXOH8rO01y0N5EZ2TT7yVx8xIrDASKRl4t~VQryRaK6kMWrgJ5EEmJTZDWHXnBI3aB7HS3PyHpnHZigCs8MiLGMJm7P0IMf5NV9XTUOXFbCBf7E1Zww__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA



# Begin Modular Function Code
def find_power_trend_line(x_data, y_data):
    popt, pcov = so.curve_fit(lambda fx,a,b: a*fx**-b,  x_data,  y_data, method="lm")
    x = np.arange(0, 2, 0.1)
    power_y = popt[0]*x**-popt[1]
    plt.scatter(x_data, y_data, label='actual data')
    plt.plot(x, power_y, label='power-fit')
    plt.legend()
    plt.show()
    print("optimal equation is: y = {} * x^(-{})".format(popt[0],popt[1]))
    return popt


def find_capture_voltage(popt, duration_val):
    capture_voltage = popt[0]*duration_val**-popt[1]
    capture_voltage = round(capture_voltage,2)
    print("The capture voltage at {} s is {} V".format(duration_val, capture_voltage))
    return capture_voltage


def find_rheobase_chronaxie(popt):
    # Calculate Rheobase
    inf_duration = 5
    rheobase = popt[0]*inf_duration**-popt[1]
    rheobase = round(rheobase, 2)
    print("Rheobase = {}".format(rheobase))
    # Calculate Chronaxie
    # (2 * Rheobase) = A * chronaxie^(B)
    chronaxie = (2*rheobase / popt[0])**(1/popt[1])
    chronaxie = round(chronaxie, 2)
    print("Chronaxie = {}".format(chronaxie))
    return rheobase, chronaxie


#def generate_capture():



def main_patient_1():
    """
    This function will drive the energy saving algorithm
    """
    pulse_duration = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.4]      # [s] Pulse duration of patient 1
    voltage_amp = [4.75, 3.25, 2.7, 2.5, 2.3, 2.1, 2.1]     # [V] Voltage amplitude of patient 1
    exponential_params = find_power_trend_line(pulse_duration, voltage_amp)
    capture_voltage = find_capture_voltage(exponential_params,0.4)
    rheobase, chronaxie = find_rheobase_chronaxie(exponential_params)


if __name__ == "__main__":
    main_patient_1()
