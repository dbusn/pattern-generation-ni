# Functions to create patterns for phonemes
# Imports
import numpy as np
import gifutils
import argparse
import json
import random
from gen_config import *

def sin_modulation(
    total_time: int,
    modulation: int,
    fraction: float,
    phi: float,
    dis: int,
    coord_list: list,
    pho_freq: int,
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

    # From input
    time = total_time / 1000

    # Known
    max_amp = 250

    # Can be calculated from input
    period = 1 / modulation
    B = 2 * np.pi * modulation
    A = (max_amp - fraction * max_amp) / 2
    D = max_amp - A

    # For creating wave
    start = 0
    stop = time
    x = np.linspace(start, stop, int(time * 1000 / dis))

    # Create amplitude list
    amplitude_list = []
    for i in range(len(x)):
        amplitude_list.append((int)(A * np.sin(B * (x[i] - phi)) + D))

    data = []
    motors = []
    for i in range(len(amplitude_list)):
        iteration = {"iteration": [], "time": 10}

        for coords in coord_list:
            motors.append(
                {"coord": coords, "amplitude": amplitude_list[i], "frequency": pho_freq}
            )

        if pathLike is True:
            for i in range(len(coord_list)):
                iteration = {"iteration": [], "time": 10}
                motor = {
                    "coord": coord_list[i],
                    "amplitude": random.choice(amplitude_list),
                    "frequency": pho_freq,
                }
                iteration["iteration"].append(motor)
                data.append(iteration)
        else:
            active_motors = random.choices(motors, k=random.randint(1, len(motors)))
            for active_motor in active_motors:
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
                new_h = random.randint(last_h, last_h + 1)

            else:
                new_h = random.randint(last_h - 1, last_h + 1)

            if last_w == grid_width:
                # new_w = random.choice([random.randint(last_w - 1, last_w), 1])
                new_w = random.randint(last_w - 1, last_w)
            elif last_w == 1:
                # new_w = random.choice([random.randint(last_w, last_w + 1), 4])
                new_w = random.randint(last_w, last_w + 1)
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
        pathLike=pathPattern,
    )

    return all_waves


def create_static_pattern():
    coord_list = []
    all_waves = []

    coord_list = [
        (random.randint(1, grid_width), random.randint(1, grid_height))
        for _ in range(actuators_no)
    ]

    all_waves = sin_modulation(
        total_time,
        modulation,
        fraction,
        phase_change,
        discretization_rate,
        coord_list,
        frequency,
        pathLike=False,
    )

    return all_waves

def initArgsParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate dynamic patterns")
    parser.add_argument(
        "-n", type=int, nargs="?", help="number of patterns to generate", required=True
    )
    parser.add_argument(
        "--pathLike",
        default=False,
        action="store_true",
        help="generate path-like patterns",
        required=False,
    )
    parser.add_argument(
        "--jsonOnly",
        default=False,
        action="store_true",
        help="generate only json files",
        required=False,
    )

    parser.add_argument(
        "--static",
        default=False,
        action="store_true",
        help="generate static patterns",
        required=False
    )

    return parser

if __name__ == "__main__":
    
    parser = initArgsParser()
    args = parser.parse_args()

    if(args.pathLike is True and args.static is True):
        print('Static patterns cannot be path-like. Generating static patterns...')

    pathPattern = args.pathLike
    for n in range(args.n):
        if args.static is True:
            all_waves = create_static_pattern()
        else:
            all_waves = create_dynamic_pattern(pathPattern)

        json_pattern = {"pattern": all_waves}
        with open("p_" + str(n) + ".json", "w") as f:
            json.dump(json_pattern, f)

        if args.jsonOnly is False:
            with open("p_" + str(n) + ".json", "r") as f:
                json_pattern = json.load(f)

            iters = [iteration["iteration"] for iteration in json_pattern["pattern"]]
            grids = [
                [[[255, 255, 255] for _ in range(0, 4)] for _ in range(0, 6)]
                for _ in range(0, len(iters))
            ]

            for i, iteration in enumerate(iters):
                for iter in iteration:
                    col_coord = int(iter["coord"][0])
                    row_coord = int(iter["coord"][1])
                    amp = iter["amplitude"]
                    grids[i][row_coord - 1][col_coord - 1] = [
                        255 - amp,
                        255 - amp,
                        255 - amp,
                    ]

            gifutils.save_frames_as_gif(
                gifutils.frames_from_lists(grids), "gifs", "p_" + str(n)
            )
