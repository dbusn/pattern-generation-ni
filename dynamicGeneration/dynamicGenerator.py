# Functions to create patterns for phonemes
# Most patterns implemented as example are taken from [A Phonemic-Based Tactile Display for Speech Communication](https://ieeexplore.ieee.org/abstract/document/8423203) by Reed et al.

# Imports
import json
import random

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, fftshift

# With spacing $L/N$, we have the Hann window (also known as $\cos^2$ window):
#
# $w[n] = \frac{1}{2} (1 - \cos(\frac{2 \pi n}{N})), \quad 0 \leq n \leq N$.
#
# https://en.wikipedia.org/wiki/Hann_function


def simple_hann_window(coord_list, pho_freq, disc_hann, total_time):
    """
    coord_list: list of coordinates, e.g. [11, 12, 13, 14]
    pho_freq: frequency of phoneme, e.g. 300
    disc_hann: discretization rate of Hanning window, default 24
    total_time: duration of pattern in ms, e.g. 392

    returns: list of data needed to create the .json in the right format
    """
    max_amp = 250  # maximum amplitude, for our motors 250
    window = np.hanning(disc_hann)  # creating normalized hanning window
    cos_window = max_amp * window  # scaling to maximum amplitude

    data = []
    for i in range(len(cos_window)):
        iteration = {"iteration": [], "time": 20}
        motor = {
            "coord": coord_list[0],
            "amplitude": int(cos_window[i]),
            "frequency": pho_freq,
        }
        if len(coord_list) == 2:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
        if len(coord_list) == 3:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor3 = {
                "coord": coord_list[2],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
        if len(coord_list) == 4:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor3 = {
                "coord": coord_list[2],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor4 = {
                "coord": coord_list[3],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
        if len(coord_list) == 8:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor3 = {
                "coord": coord_list[2],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor4 = {
                "coord": coord_list[3],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor5 = {
                "coord": coord_list[4],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor6 = {
                "coord": coord_list[5],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor7 = {
                "coord": coord_list[6],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
            motor8 = {
                "coord": coord_list[7],
                "amplitude": int(cos_window[i]),
                "frequency": pho_freq,
            }
        iteration["iteration"].append(motor)
        if len(coord_list) == 2:
            iteration["iteration"].append(motor2)
        if len(coord_list) == 3:
            iteration["iteration"].append(motor2)
            iteration["iteration"].append(motor3)
        if len(coord_list) == 4:
            iteration["iteration"].append(motor2)
            iteration["iteration"].append(motor3)
            iteration["iteration"].append(motor4)
        if len(coord_list) == 8:
            iteration["iteration"].append(motor2)
            iteration["iteration"].append(motor3)
            iteration["iteration"].append(motor4)
            iteration["iteration"].append(motor5)
            iteration["iteration"].append(motor6)
            iteration["iteration"].append(motor7)
            iteration["iteration"].append(motor8)
        data.append(iteration)

    return data


def create_simple_hann_pattern(phoneme, coord_list, pho_freq, disc_hann, total_time):
    """
    phoneme: name of phoneme, e.g. 'CH'
    coord_list: list of coordinates, e.g. [11, 12, 13, 14]
    pho_freq: frequency of phoneme, e.g. 300
    disc_hann: discretization rate of Hanning window, default 24
    total_time: duration of pattern in ms, e.g. 392

    returns: creates .json file of phoneme
    """
    all_waves = simple_hann_window(coord_list, pho_freq, disc_hann, total_time)
    json_pattern = {"pattern": all_waves}
    with open(phoneme + ".json", "w") as f:
        json.dump(json_pattern, f)


def overlapping_hann_pattern(coord_list, pho_freq, disc_hann, total_time, step):
    """
    coord_list: list of coordinates, e.g. [11, 12, 13, 14]
    pho_freq: frequency of phoneme, e.g. 300
    disc_hann: discretization rate of Hanning window, default 12
    total_time: duration of pattern in ms, e.g. 392
    step: timestep for a new Hanning window to be added

    returns: list of data needed to create the .json in the right format
    """
    max_amp = 250  # maximum amplitude, for our motors 250
    window = np.hanning(disc_hann)  # creating normalized hanning window
    cos_window = max_amp * window  # scaling to maximum amplitude

    nCoords = len(coord_list)
    bool_list = [
        False for i in range(nCoords)
    ]  # list to keep track whether coordinate is 'done'
    print(total_time / disc_hann)  # to check it's an integer
    print(step / disc_hann)  # to check it's an integer
    disc_time = total_time // disc_hann
    disc_step = step // disc_hann
    amp_list = [
        [0] * disc_time for _ in range(nCoords)
    ]  # amplitude for each discretized timestep, for each coordinate
    # loop over all coordinates, and then over all timesteps, and assign amplitude
    for coord in range(nCoords):
        for timestep in range(disc_time - sum(bool_list) * disc_step):
            amp_list[coord][timestep + sum(bool_list) * disc_step] = cos_window[
                timestep if timestep < disc_hann else 0
            ]
        bool_list[coord] = True

    # NOTE: here it is assumed that for coordinate x, x+1 is simultaneously vibrating
    data = []
    for t in range(disc_time):
        iteration = {"iteration": [], "time": 5}  # 5 is default, can be changed.
        for i in range(nCoords):
            if int(amp_list[i][t]) != 0:  # filter out amplitude = 0
                motor = {
                    "coord": coord_list[i],
                    "amplitude": int(amp_list[i][t]),
                    "frequency": pho_freq,
                }
                motor2 = {
                    "coord": coord_list[i] + 1,
                    "amplitude": int(amp_list[i][t]),
                    "frequency": pho_freq,
                }
                iteration["iteration"].append(motor)
                iteration["iteration"].append(motor2)
        data.append(iteration)

    return data


def create_overlapping_hann_pattern(
    phoneme, coord_list, pho_freq, disc_hann, total_time, step
):
    """
    phoneme: name of phoneme, e.g. 'OE'
    coord_list: list of coordinates, e.g. [11, 12, 13, 14]
    pho_freq: frequency of phoneme, e.g. 300
    disc_hann: discretization rate of Hanning window, default 24
    total_time: duration of pattern in ms, e.g. 392
    step: timestep for a new Hanning window to be added

    returns: creates .json file of phoneme
    """
    all_waves = overlapping_hann_pattern(
        coord_list, pho_freq, disc_hann, total_time, step
    )
    json_pattern = {"pattern": all_waves}
    with open(phoneme + ".json", "w") as f:
        json.dump(json_pattern, f)


# Below, there is a helpful function to plot sinuses, afterwards the sinusiodal pattern generation functions are given.
#
# $y = A \sin(B(x - \phi)) + D$
def plot_sinus(total_time, modulation, fraction, phi, dis):
    """
    total_time: total time of sinus in ms, e.g. 392
    modulation: modulation of wave in Hz, e.g. 30
    fraction: fraction of the max amplitude of the motors to be the minimum of the wave, default 0.5
    phi: phase change, e.g. 0.4*(1 / modulation)
    dis: discretization rate, default for 092 time waves is 6, default for 392 time waves is 12

    returns: list of data needed to create the .json in the right format
    """

    # from input
    time = time / 1000  # s

    # known
    max_amp = 250

    # can be calculated from input
    period = 1 / modulation
    B = 2 * np.pi * modulation
    A = (max_amp - fraction * max_amp) / 2
    D = max_amp - A

    # for creating wave
    start = 0
    stop = time
    x = np.linspace(start, stop, int(time * 1000 / dis))

    # create amplitude list
    amplitude_list = []
    for i in range(len(x)):
        amplitude_list.append(A * np.sin(B * (x[i] - phi)) + D)

    # plotting
    plt.plot(x, A * np.sin(B * (x - phi)) + D)
    plt.title("wave")
    plt.xlabel("time(s)")
    plt.ylabel("amplitude")
    plt.show()


def sin_modulation(
    total_time: int,
    modulation: int,
    fraction: float,
    phi: float,
    dis: int,
    coord_list: list,
    pho_freq: int,
    dynamic: bool,
    pathLike: bool,
):
    """
    total_time: total time of sinus in ms, e.g. 392
    modulation: modulation of wave in Hz, e.g. 30
    fraction: fraction of the max amplitude of the motors to be the minimum of the wave, default 0.5
    phi: phase change, e.g. 0.4*(1 / modulation)
    dis: discretization rate, default for 092 time waves is 6, default for 392 time waves is 12
    coord_list: list of coordinates, e.g. [12, 13, 14, 15]
    pho_freq: frequency of phoneme, e.g. 300
    dynamic: generate siple or dynamic pattern
    pathLike: generate pathLike or completely random pattern

    returns: makes a plot of how the sinus looks like
    """

    # from input
    if dynamic is True:
        time = total_time / 1000
    else:
        time = total_time

    # known
    max_amp = 250

    motors = []

    # can be calculated from input
    period = 1 / modulation
    B = 2 * np.pi * modulation
    A = (max_amp - fraction * max_amp) / 2
    D = max_amp - A

    # for creating wave
    start = 0
    stop = time
    x = np.linspace(start, stop, int(time * 1000 / dis))
    #     print(x)

    # create amplitude list
    amplitude_list = []
    for i in range(len(x)):
        amplitude_list.append((int)(A * np.sin(B * (x[i] - phi)) + D))

    data = []
    for i in range(len(amplitude_list)):
        iteration = {"iteration": [], "time": 10}
        motor = {
            "coord": coord_list[0],
            "amplitude": amplitude_list[i],
            "frequency": pho_freq,
        }
        motors.append(motor)
        if len(coord_list) == 2:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motors.append(motor2)
        if len(coord_list) == 3:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor3 = {
                "coord": coord_list[2],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motors.append(motor2)
            motors.append(motor3)
        if len(coord_list) == 4:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor3 = {
                "coord": coord_list[2],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor4 = {
                "coord": coord_list[3],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motors.append(motor2)
            motors.append(motor3)
            motors.append(motor4)
        if len(coord_list) == 8:
            motor2 = {
                "coord": coord_list[1],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor3 = {
                "coord": coord_list[2],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor4 = {
                "coord": coord_list[3],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor5 = {
                "coord": coord_list[4],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor6 = {
                "coord": coord_list[5],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor7 = {
                "coord": coord_list[6],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motor8 = {
                "coord": coord_list[7],
                "amplitude": amplitude_list[i],
                "frequency": pho_freq,
            }
            motors.append(motor2)
            motors.append(motor3)
            motors.append(motor4)
            motors.append(motor5)
            motors.append(motor6)
            motors.append(motor7)
            motors.append(motor8)

        if pathLike is True:
            for i in range(len(coord_list)):
                iteration = {"iteration": [], "time": 10}
                motor = {
                    "coord": coord_list[i],
                    "amplitude": random.choice(amplitude_list),
                    "frequency": pho_freq,
                }
                # print(motor)
                iteration["iteration"].append(motor)
                data.append(iteration)
        else:
            for active_motor in motors:
                iteration["iteration"].append(active_motor)
            data.append(iteration)

    return data


def create_simple_sin_modulation(
    phoneme, total_time, modulation, fraction, phi, dis, coord_list, pho_freq
):
    """
    phoneme: name of the phoneme, e.g. 'B'
    total_time: total time of sinus in ms, e.g. 392
    modulation: modulation of wave in Hz, e.g. 30
    fraction: fraction of the max amplitude of the motors to be the minimum of the wave, default 0.5
    phi: phase change, e.g. 0.4*(1 / modulation)
    dis: discretization rate, default for 092 time waves is 6, default for 392 time waves is 12
    coord_list: list of coordinates, e.g. [12, 13, 14, 15]
    pho_freq: frequency of phoneme, e.g. 300

    returns: creates a .json file of phoneme
    """
    all_waves = sin_modulation(
        total_time, modulation, fraction, phi, dis, coord_list, pho_freq, False
    )
    json_pattern = {"pattern": all_waves}
    with open(phoneme + ".json", "w") as f:
        json.dump(json_pattern, f)


def create_dynamic_pattern(pathPattern: bool) -> list:
    modulation: int = 60
    total_time: int = random.choice(seq=[50, 60, 70, 80])
    fraction: float = 0.5
    phase_change: int = random.choice(seq=[0, 0.2, 0.4, 0.6, 0.8]) * (1 / modulation)
    discretization_rate: int = 6
    actuators_no: int = random.choice(seq=[2, 3, 4, 8])
    grid_height: int = 6
    grid_width: int = 4
    frequency: int = random.choice(seq=[300])
    patterns_no = 8
    coord_list = []
    all_waves = []

    if pathPattern is True:
        if len(coord_list) == 0:
            coord_list = [
                (random.randint(1, grid_width), random.randint(1, grid_height))
            ]

        # Select which actuators are active
        # actuators_no = number of active actuators
        for _ in range(actuators_no):
            last_w = coord_list[-1:][0][0]
            last_h = coord_list[-1:][0][1]

            # print("H:" + str(last_h) + " W:" + str(last_w))

            if last_h == grid_height:
                # new_h = random.choice([random.randint(last_h - 1, last_h), 1])
                new_h = random.randint(last_h - 1, last_h)
            elif last_h == 1:
                # new_h = random.choice([random.randint(last_h, last_h + 1), 6])
                new_h = random.randint(last_h, last_h+1)

            else:
                new_h = random.randint(last_h - 1, last_h + 1)

            if last_w == grid_width:
                # new_w = random.choice([random.randint(last_w - 1, last_w), 1])
                new_w = random.randint(last_w-1, last_w)
            elif last_w == 1:
                # new_w = random.choice([random.randint(last_w, last_w + 1), 4])
                new_w = random.randint(last_w, last_w+1)
            else:
                new_w = random.randint(last_w - 1, last_w + 1)

            coord_list.append((new_w, new_h))
    else:
        for _ in range(patterns_no):
            coord_list = [
                (random.randint(1, grid_width), random.randint(1, grid_height))
                for _ in range(actuators_no)
            ]

    all_waves += sin_modulation(
        total_time,
        modulation,
        fraction,
        phase_change,
        discretization_rate,
        coord_list,
        frequency,
        dynamic=True,
        pathLike=pathPattern,
    )

    return all_waves


if __name__ == "__main__":
    n_gifs = 10
    for i in range(n_gifs):
        all_waves = create_dynamic_pattern(pathPattern=True)
        json_pattern = {"pattern": all_waves}
        with open("p_" + str(i) + ".json", "w") as f:
            json.dump(json_pattern, f)
