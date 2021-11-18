# energy_saver_algorthm.py
# Author: Alex Thomason


# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as so
import logging
from mpl_toolkits . mplot3d import Axes3D


# Begin Modular Function Code

def find_power_trend_line(pulse_duration_experimental,
                          voltage_amp_experimental):
    """ Finds the formula to describe the strength duration curve by
        optimizing rheobase and chronaxie

    Strength Duration curve formula: V = Vr * (1 + t_c/t)
        - V = threshold Voltage at pulse duration t
        - Vr = rheobase Voltage
        - t_c = chronaxie pulse duration
        - t = stimulation pulse duration
        - Forumula Source:
        https://thoracickey.com/2-components-of-a-pacing-and-icd-system-basic-concepts-of-pacing/

    This function takes in experimental data of pulse duration
    and voltage amplitudethat has been measured from a patient
    using a pacemaker.The scipy.optimize.curve_fit module optimizes
    rheobase and chronaxie to the strength duration curve formula
    (described above) using the experimental data.

    Args:
        pulse_duration_experimental (list): list of experimental pulse
                                            duration data
        voltage_amp_experimental (list): list of experimental voltage
                                         amplitude data
    Returns:
        rheobase (float): optimized rheobase value based on the
                          experimental data
        chronaxie (float): optimized chronaxie value based on the
                           experimental data
    """
    popt, pcov = so.curve_fit(lambda t, rheobase, chronaxie:
                              rheobase * (1 + chronaxie/t),
                              pulse_duration_experimental,
                              voltage_amp_experimental,
                              method="lm")
    rheobase = round(popt[0], 2)
    chronaxie = round(popt[1], 2)
    print("optimal equation is: V = {} * (1 + {}/t)".format(rheobase,
                                                            chronaxie))
    print("Rheobase = {} V".format(rheobase))
    print("Chronaxie = {} ms".format(chronaxie))
    return rheobase, chronaxie


def calculate_capture_voltage(rheobase, chronaxie, duration_val):
    """
    Finds the minimum voltage it takes to capture mycardial tissue.
    In other words, this function finds the voltage amplitude for a
    pulse duration. If a float is entered for duration_val, a float
    capture_voltage will be returned. If a list is entered for
    duration_val, a list capture_voltage will be returned.

    Args:
        rheobase (float): rheobase value
        chronaxie (float): chronaxie value
        duration value (float or list): duration value

    Returns:
        capture_voltage (float or list): voltage amplitude to capture the
                                 myocardial tissue at the given
                                 duration value
    """
    capture_voltage = rheobase * (1 + chronaxie/duration_val)
    if type(duration_val) == list or np.ndarray:
        return capture_voltage
    elif type(duration_val) == float or int:
        capture_voltage = round(capture_voltage, 2)
        return capture_voltage


def calculate_energy(pulse_duration,
                     voltage_amp,
                     pacing_resistance):
    """
    Finds the energy it for a given pulse duration and voltage
    amplitude. pulse_duration and voltage_amp can be entered
    either as floats or as a list. If they are entered as
    floats, then energy will be returned as a float. If they
    are entered as lists, then energy will be returned as a
    list.

    Energy Equation:
        E = V^2 * t / R
        - V = threshold Voltage at pulse duration t
        - R = total pacing impedence (generally ~1000 ohms is a good
              approximation)
        - t = stimulation pulse duration
        - Forumula Source:
        https://thoracickey.com/2-components-of-a-pacing-and-icd-system-basic-concepts-of-pacing/

    Args:
        pulse_duration (float or list): stimulus pulse duration
        voltage_amp (float or list): stimulus voltage amplitude
        pacing_resistance (float or int): total pacing impedence

    Returns:
        Energy (float or list): energy [joules] it for a given pulse
                                duration and voltage amplitude
    """
    energy = voltage_amp**2 * (pulse_duration * 10**(-3)) / pacing_resistance
    return energy


def plot_strength_duration_curve(pulse_duration_experimental,
                                 voltage_amp_experimental,
                                 pulse_duration_interp,
                                 voltage_amp_interp):
    plt.plot(pulse_duration_experimental, voltage_amp_experimental,
             'o', label="Experimental Data")
    plt.plot(pulse_duration_interp, voltage_amp_interp, '-',
             label="Optimized Trendline")
    plt.xlabel('Pulse Duration [ms]')
    plt.ylabel('Voltage Amplitude [ms]')
    plt.legend()
    plt.show()


def plot_energy_curve(pulse_duration, voltage_amp, pacing_resistance):

    fig = plt.figure()
    ax = Axes3D(fig)
    pulse_duration, voltage_amp = np.meshgrid(pulse_duration, voltage_amp)
    energy = calculate_energy(pulse_duration, voltage_amp, pacing_resistance)
    energy_surface = ax.plot_surface(pulse_duration, voltage_amp, energy)
    plt.xlabel('Pulse Duration [ms]')
    plt.ylabel('Voltage Amplitude [ms]')
    plt.show()


def patient_data_manipulation(pulse_duration_experimental,
                              voltage_amp_experimental):
    """
    This function takes in experimental data and finds rheobase,
    chronaxie, minimum pacing energy, plots strength duration curve,
    and plots energy curve.
    """
    rheobase, chronaxie = find_power_trend_line(pulse_duration_experimental,
                                                voltage_amp_experimental)
    pacing_resistance = 1000   # [ohms] total pacing impedence
    min_pulse_energy = calculate_energy(rheobase, chronaxie, pacing_resistance)
    print("Minimum pacing energy to stimulate myocardial \
tissue is {} Joules".format(min_pulse_energy))
    pulse_duration_optimized = np.arange(0.1, 2, 0.1)
    voltage_amp_optimized = calculate_capture_voltage(rheobase,
                                                      chronaxie,
                                                      pulse_duration_optimized)
    pulse_energy = calculate_energy(pulse_duration_optimized,
                                    voltage_amp_optimized, pacing_resistance)
    plot_strength_duration_curve(pulse_duration_experimental,
                                 voltage_amp_experimental,
                                 pulse_duration_optimized,
                                 voltage_amp_optimized)
    plot_energy_curve(pulse_duration_optimized, voltage_amp_optimized,
                      pacing_resistance)
    return rheobase, chronaxie, min_pulse_energy


if __name__ == "__main__":
    # Sample Strength-duration data
    
    # patient 1
    # https://d1wqtxts1xzle7.cloudfront.net/50956640/j.1540-8159.2009.02456.x2x0161218-19709-1lbuxg3-with-cover-page-v2.pdf?Expires=1635175866&Signature=N-ROBbokpqOa-5ioS8HXjMkeKh2I7sGkPqwLSjghrTBY7wRHJ75ELUi2FyERHH3acmAdyosEmHjI14bsrWXjqBZfxheNTCjoXw8qNEmJFiRXeWNbcy4kvfvMrdIDYqUcCFME-~beHZc51a4AazX4JsYplcBhMsVn9ljTvyy-tW4x21UFg31FaQzLI~yt2mevWPPXGYqpeoK62G7PesuSft~r-6g-HHU6DoBxXOH8rO01y0N5EZ2TT7yVx8xIrDASKRl4t~VQryRaK6kMWrgJ5EEmJTZDWHXnBI3aB7HS3PyHpnHZigCs8MiLGMJm7P0IMf5NV9XTUOXFbCBf7E1Zww__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA

    """    
    # [ms] Pulse duration of patient 1
    duration_experimental = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.4]
    # [V] Voltage amplitude of patient 1
    voltage_experimental = [5, 3.5, 2.8, 2.6, 2.4, 2.2, 2.2]
    rheobase1, chronaxie1, min_pulse_energy = patient_data_manipulation(duration_experimental,
                                                      voltage_experimental)
    """

    # [ms] Pulse duration of patient 1
    duration_experimental = [ 0.2, 0.4, 1]
    # [V] Voltage amplitude of patient 1
    voltage_experimental = [3.5, 2.6, 2.2]
    rheobase1, chronaxie1, min_pulse_energy = patient_data_manipulation(duration_experimental,
                                                      voltage_experimental)
