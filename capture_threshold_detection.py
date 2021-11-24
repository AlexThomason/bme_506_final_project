# find_experimental_capture_data.py
# Author: Alex Thomason


# Import necessary packages
import logging
import import_capture_data as icd
import generate_capture_data as gcd
import strength_duration_curve as sdc


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
                myocardium, then the experimental voltage is set to 1 V
                higher than the previous experimental voltage
        - If the experimental voltage is not enough to stimulate the
                myocardium, then a backup voltage of 4.5 V is given to
                the patient to ensure that pacing occurs.
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
        capture_duration (float): duration of the capture voltage
        capture_voltage (float): capture voltage of the myocardial tissue
                within a 5% error above the true cpature voltage
    """
    # Experimental duration (kept constant while stimulus voltage is
    # changed)
    duration_experimental = duration_list[0]
    logging.info("Finding Capture Voltage for a stimulus duration \
of {} ms".format(duration_experimental))
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
stimulus of {} V for {} ms".format(voltage_experimental,
                                   duration_experimental))
            capture_voltage_experimental_list.append(voltage_experimental)

            if small_step_indicator == 0:
                voltage_experimental *= 0.75

            if small_step_indicator == 1:
                voltage_experimental *= 0.95

        if capture_status == 0:
            logging.warn("Failed to Capture: Myocardial tissue was not \
captured with stimulus of {} V for {} ms. A backup pulse of 4.5 V was \
applied to the patient".format(voltage_experimental, duration_experimental))

            # Increases the voltage to 5 Volts if the beginning voltage is
            # insufficient for myocardial stimulation
            if len(capture_voltage_experimental_list) == 0:
                logging.warn("Start voltage of {} V did not stimulate \
the myocardial tissue at at stimulation duration of {} ms. The next \
stimulus voltage is set to be 5 V.".format(voltage_experimental,
                                           duration_experimental,
                                           voltage_experimental + 1))
                voltage_experimental += 1
                continue

            else:
                no_capture_counter += 1
                voltage_experimental = \
                    capture_voltage_experimental_list[-1] * 0.95
                small_step_indicator = 1

    print("Capture Voltage Experimental List: \
{}".format(capture_voltage_experimental_list))
    logging.info("Capture Voltage Experimental List: \
{}".format(capture_voltage_experimental_list))

    capture_voltage = capture_voltage_experimental_list[-1]
    print("The capture voltage within 5 percent error \
is: {}".format(capture_voltage))
    logging.info("The capture voltage within 5 percent error \
is: {}\n".format(capture_voltage))

    return duration_experimental, capture_voltage


def find_patient_capture_voltage(filename: str):
    """Finds the capture voltage of a patient data file

    Args:
        filename (str): patient data file ending in .csv

        Note: The patient data should have the following columns:
        (1) stimulus duration - constant pulse duration
        (2) Stimulus Voltage Amplitude - varying voltage of the stimulus
        (3) Capture Status (1 = capture, 0 = no capture)

    Returns:
        capture_duration (float): duration of the capture voltage
        capture_voltage (float): capture voltage of the myocardial tissue
                for a pulse duration (duration value is specified in the
                first column of the patient data file)
    """
    duration_list, voltage_list, capture_list = icd.import_parse_convert_data(
                                                filename)
#    logging.basicConfig(filename="log_files/{}.log".format(
#                        filename[:-4]), filemode="r",
#                        level=logging.INFO)
    capture_duration, capture_voltage = \
        find_capture_voltage(duration_list, voltage_list,
                             capture_list)
    return capture_duration, capture_voltage


def patient_strength_duration_data(patient_name: str,
                                   patient_data_filename_list: list):
    """

    """
    logging.basicConfig(filename="log_files/{}.log".format(
                        patient_name), filemode="w",
                        level=logging.INFO)
    capture_duration_data = []
    capture_voltage_data = []

    for filename in patient_data_filename_list:
        capture_duration, capture_voltage = \
                    find_patient_capture_voltage(filename)
        capture_duration_data.append(capture_duration)
        capture_voltage_data.append(capture_voltage)

    print("The capture duration data (in ms) {} is: {}".format(
        patient_name, capture_duration_data))
    logging.info("The capture duration data (in ms) {} is: {}".format(
        patient_name, capture_duration_data))
    print("The capture voltage data (in Volts) for {} is: {}".format(
        patient_name, capture_duration_data))
    logging.info("The capture voltage data (in Volts) for {} is: {}\n".format(
        patient_name, capture_voltage_data))

    rheobase, chronaxie, min_pulse_energy = sdc.patient_data_manipulation(
        capture_duration_data,
        capture_voltage_data)

    voltage_at_chronaxie = 2*rheobase
    reccomended_pulse_duration = 3 * chronaxie
    energy_at_pulse_reccomendation = sdc.calculate_energy(
        reccomended_pulse_duration, voltage_at_chronaxie, 1000)

    logging.info("RHEOBASE / CHRONAXIE / MIN ENERGY- {}".format(patient_name))
    logging.info("{} Rheobase = {} V".format(patient_name, rheobase))
    logging.info("{} Chronaxie = {} ms".format(patient_name, chronaxie))
    logging.info("Voltage at Chronaxie = {} V".format(voltage_at_chronaxie))
    logging.info("{} Minimum Pulse Energy = {} J\n".format(patient_name,
                                                           min_pulse_energy))
    logging.info("RECCOMENDED SETTINGS - {}".format(patient_name))
    logging.info("Recomended stimulus duration for {} = {} ms".format(
        patient_name, reccomended_pulse_duration))
    logging.info("Recomended Voltage for {} = {} V".format(
        patient_name, voltage_at_chronaxie))
    logging.info("Energy at reccomended pulse duration and voltage \
for {} = {} J".format(patient_name, energy_at_pulse_reccomendation))

    return rheobase, chronaxie


if __name__ == "__main__":
    # ____PATIENT 1____

    p1_data_filename_list = ["patient1_0.1ms.csv",
                             "patient1_0.2ms.csv",
                             "patient1_0.3ms.csv",
                             "patient1_0.4ms.csv",
                             "patient1_0.5ms.csv",
                             "patient1_1ms.csv",
                             "patient1_1.4ms.csv"]
    p1_rheobase, p1_chronaxie = patient_strength_duration_data(
        "patient1", p1_data_filename_list)
    
    """
    p1_data_filename_list = ["patient1_0.2ms.csv",
                             "patient1_0.3ms.csv",
                             "patient1_0.5ms.csv",
                             "patient1_1ms.csv",
                             "patient1_1.4ms.csv"]
    p1_rheobase, p1_chronaxie = patient_strength_duration_data(
        "patient1", p1_data_filename_list)

    p1_data_filename_list = ["patient1_0.2ms.csv",
                             "patient1_0.5ms.csv",
                             "patient1_1ms.csv",
                             "patient1_1.4ms.csv"]
    p1_rheobase, p1_chronaxie = patient_strength_duration_data(
        "patient1", p1_data_filename_list)


    p1_data_filename_list = ["patient1_0.2ms.csv",
                             "patient1_0.5ms.csv",
                             "patient1_1ms.csv"]
    p1_rheobase, p1_chronaxie = patient_strength_duration_data(
        "patient1", p1_data_filename_list)

    p1_data_filename_list = ["patient1_0.2ms.csv",
                             "patient1_1ms.csv"]
    p1_rheobase, p1_chronaxie = patient_strength_duration_data(
        "patient1", p1_data_filename_list)
    """

    # ____PATIENT 2____
    """
    p1_data_filename_list = ["patient2_0.3ms.csv",
                             "patient2_0.5ms.csv",
                             "patient2_0.8ms.csv",
                             "patient2_1ms.csv",
                             "patient2_1.5ms.csv"]
    p2_rheobase, p2_chronaxie = patient_strength_duration_data(
        "patient2", p1_data_filename_list)
    """
