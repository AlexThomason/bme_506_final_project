# find_experimental_capture_data.py
# Author: Alex Thomason


# Import necessary packages
import numpy as np
import logging
import import_capture_data as icd
import generate_capture_data as gcd


"""def deliver_backup_pulse(failed_duration, failed_voltage):
    logging.info("A stimulus of {} V for {} ms did not capture \
                  the myocardial tissue. A backup pulse of 4.5 V \
                  was applied to the patient".format(
                  failed_duration, failed_voltage))


def detect_capture(voltage_list, capture_list, trial_voltage):
    if capture_list[voltage_list.index(trial_voltage)] == 0:
        return False
    if capture_list[voltage_list.index(trial_voltage)] == 1:
        return True"""


def find_capture_voltage(duration_list: list, voltage_list: list,
                         capture_list: list):
    """Finds the capture voltage of a patient at a certain stimulus duration.

    This function contains the algorithm to find the capture voltage
    threshold of a patients myocardial tissue. In real life, a
    pacemaker could use a version of this algrithm to find the stimuls
    thresholds at various stimulation pulse durations. This function
    detects if a voltage has been captured by viewing the capture status
    of the previously generated data. Reference the module
    "generate_capture_data.py" to see how that data is generated.
    In a real pacemaker, a capture detection algorithm of the heart's
    electrical signals would be used to determine whether or not the
    tissue has been captured.

    Summary of how this function works:
        - Start voltage is pre-determined to be 3 V
        - no_capture_counter is set to 0
        - Other relavent variables are pre-determined (see # descriptions)
        - While loop initiated --> continues to run as long as
                the no_capture_counter is less than 2
        - If the starting voltage is not strong enough to stimulate the
                myocardium, then the experimental voltage is set to 5 V
        - If the experimental voltage (or starting voltage) is not
                enough to stimulate the myocardium, then a backup
                voltage of 5V is given to the patient to ensure
                that pacing occurs.
        - Finds returns the capture voltage of the myocardial tissue
                within a 5% error above the true cpature voltage

    Args:
        duration_list (list): list of constant pulse durations
        voltage_list (list): stimulus voltage amplitude that is the
                             varying voltage of the stimulus
        capture_list (list): List of Capture Status values coresponding
                             to the duration_list and voltage_list
                             (1 = capture, 0 = no capture)

    Returns:
        capture_voltage (float): capture voltage of the myocardial tissue
                within a 5% error above the true cpature voltage
    """
    # [V] Start voltage
    voltage_start = 3
    # [V] Experimental voltage and itterated in while loop
    voltage_experimental = voltage_start
    # [V] List to store all the voltages that capture the myocardium
    capture_voltage_experimental_list = []
    # Counter to keep track of the number of times an experimental volgate
    # does not capture the myocardium
    no_capture_counter = 0
    # Indicator to decrease the experimental voltage in smaller steps
    small_step_indicator = 0

    while no_capture_counter < 2:
        idx, voltage_experimental = gcd.find_nearest(voltage_list,
                                                     voltage_experimental)
        capture_status = capture_list[idx]

        if capture_status == 1:
            logging.info("Captured: Myocardial tissue was captured with \
stimulus of {} V for {} ms".format(voltage_experimental, duration_list[0]))
            capture_voltage_experimental_list.append(voltage_experimental)

            if small_step_indicator == 0:
                voltage_experimental *= 0.75

            if small_step_indicator == 1:
                voltage_experimental *= 0.95

        if capture_status == 0:
            logging.info("Failed to Capture: Myocardial tissue was not \
captured with stimulus of {} V for {} ms. A backup pulse of 4.5 V was \
applied to the patient".format(voltage_experimental, duration_list[0]))

            # Increases the voltage to 5 Volts if the beginning voltage is
            # insufficient for myocardial stimulation
            if len(capture_voltage_experimental_list) == 0:
                logging.info("Start voltage of {} V did not stimulate \
the myocardial tissue at at stimulation duration of {} ms. The next \
stimulus voltage is set to be 5 V.".format(voltage_experimental,
                                           duration_list[0]))
                voltage_experimental = 5
                continue

            else:
                no_capture_counter += 1
                voltage_experimental = capture_voltage_experimental_list[-1]
                small_step_indicator = 1

    print("Capture Voltage Experimental List: \
{}".format(capture_voltage_experimental_list))
    logging.info("Capture Voltage Experimental List: \
{}".format(capture_voltage_experimental_list))

    capture_voltage = capture_voltage_experimental_list[-1]
    print("The capture voltage within 5 percent error \
is: {}".format(capture_voltage))
    logging.info("The capture voltage within 5 percent error \
is: {}".format(capture_voltage))

    return capture_voltage


def find_patient_capture_voltage(filename: str):
    """Finds the capture voltage of a patient data file

    Args:
        filename (str): patient data file ending in .csv

        Note: The patient data should have the following columns:
        (1) stimulus duration - constant pulse duration
        (2) Stimulus Voltage Amplitude - varying voltage of the stimulus
        (3) Capture Status (1 = capture, 0 = no capture)

    Returns:
        capture_voltage (float): capture voltage of the myocardial tissue
                for a pulse duration (duration value is specified in the
                first column of the patient data file)
    """
    duration_list, voltage_list, capture_list = icd.import_parse_convert_data(
                                                filename)
    logging.basicConfig(filename="log_files/{}.log".format(
                        filename[:-4]), filemode="r",
                        level=logging.INFO)
    capture_voltage = find_capture_voltage(duration_list, voltage_list,
                                           capture_list)
    return capture_voltage


if __name__ == "__main__":
    filename = "patient1_0.3ms.csv"
    find_patient_capture_voltage(filename)
