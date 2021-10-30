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


def find_capture_voltage(duration_list, voltage_list, capture_list):

    voltage_start = 4           # [V] Start voltage
    voltage_experimental = voltage_start
    capture_voltage_experimental_list = []
    no_capture_counter = 0
    # small_step_indicator indicates voltage step size.
    # 0.75% voltage step when small_step_indicator = 0
    # 0.95% voltage step when small_step_indicator = 1
    small_step_indicator = 0
#    step_down_size = 0.25 * voltage_experimental
#    small_step_up_size = 0.05

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
            no_capture_counter += 1
            voltage_experimental = capture_voltage_experimental_list[-1]
            small_step_indicator = 1
    print("Capture Voltage Experimental List: \
{}".format(capture_voltage_experimental_list))
    capture_voltage = capture_voltage_experimental_list[-1]
    print("The capture voltage within 5 percent error \
is: {}".format(capture_voltage))
    return capture_voltage


def algorithm_driver(filename):
    logging.basicConfig(filename="log_files/{}.log".format(
                        filename.strip('.csv')), filemode="w",
                        level=logging.INFO)
    duration_list, voltage_list, capture_list = icd.import_parse_convert_data(
                                                filename)
    capture_voltage = find_capture_voltage(duration_list, voltage_list,
                                           capture_list)
    print(capture_voltage)


if __name__ == "__main__":
    algorithm_driver("patient1_1.4ms.csv")
