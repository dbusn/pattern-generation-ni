# Functions to create patterns for phonemes
# Imports
import numpy as np
import gifutils
import argparse
import json
import random
import scipy
import config
import scipy.signal

# from numba import jit

# @jit(nopython=True)
def process_amplitude_list(amplitude_list, coord_list, pho_freq, pathLike, static):
    data = []
    motors = []

    if pathLike is False and static is False:
        for i in range(len(coord_list)):
            motors.append(
                {
                    "coord": coord_list[i],
                    "amplitude": random.choice(amplitude_list),
                    "frequency": pho_freq,
                }
            )

    for i in range(len(amplitude_list)):
        iteration = {"iteration": [], "time": 10}

        if pathLike is True:
            for j in range(len(coord_list)):
                iteration = {"iteration": [], "time": 10}
                motor = {
                    "coord": coord_list[j],
                    "amplitude": random.choice(amplitude_list),
                    "frequency": pho_freq,
                }
                iteration["iteration"].append(motor)
                data.append(iteration)
        else:
            if static is True:
                motors = []
                for j in range(len(coord_list)):
                    motors.append(
                        {
                            "coord": coord_list[j],
                            "amplitude": random.choice(amplitude_list),
                            "frequency": pho_freq,
                        }
                    )

                for active_motor in motors:
                    iteration["iteration"].append(active_motor)
            # Regular dynamic pattern
            else:
                # Choose k random motors that are active in an iteration
                active_motors = random.choices(motors, k=random.randint(1, len(motors)))
                for active_motor in active_motors:
                    iteration["iteration"].append(active_motor)
            data.append(iteration)

    return data


def block_modulation(modulation_data: dict,):
    # Note that we assume a block function y = 1 if 0 <= x < period, -1 if period < x < 2*period
    # Calculated from input
    period = 1 / modulation_data["phase_change"]

    a = random.choice(config.amplitudes)

    # For creating wave
    time = modulation_data["total_time"] / 1000
    start = 0
    stop = time
    x = np.linspace(start, stop, modulation_data["dis"])

    # Create amplitude list
    amplitude_list = []
    for i in range(len(x)):
        if x[i] % 2 * period < period:  # if 0 <= x < period
            sign = 1
        else:  # period <= x < 2*period
            sign = -1
        amplitude_list.append((int)(a * sign))

    return process_amplitude_list(
        amplitude_list,
        modulation_data["coord_list"],
        modulation_data["freq"],
        modulation_data["path_like"],
        modulation_data["is_static"],
    )


def hanning_modulation(modulation_data: dict,):
    # Hanning window
    amplitude_list = random.choice(config.amplitudes) * np.hanning(
        modulation_data["dis"]
    )

    return process_amplitude_list(
        amplitude_list,
        modulation_data["coord_list"],
        modulation_data["freq"],
        modulation_data["path_like"],
        modulation_data["is_static"],
    )


def sawtooth_modulation(modulation_data: dict,):
    # Computed from input
    B = 2 * np.pi * modulation_data["freq"]

    # For creating a wave
    time = modulation_data["total_time"] / 1000
    start = 0
    stop = time
    x = np.linspace(start, stop, modulation_data["dis"])
    max_amp = random.choice(config.amplitudes)

    # Create amplitude list
    phi = 0
    amplitude_list = []
    for i in range(len(x)):
        amplitude_list.append(
            (int)((max_amp * scipy.signal.sawtooth(B * (x[i] - phi)) + max_amp) / 2)
        )

    return process_amplitude_list(
        amplitude_list,
        modulation_data["coord_list"],
        modulation_data["freq"],
        modulation_data["path_like"],
        modulation_data["is_static"],
    )


def sin_modulation(modulation_data: dict):
    # Calculated from input
    B = 2 * np.pi * modulation_data["modulation"]
    max_amp = random.choice(config.amplitudes)
    A = (max_amp - modulation_data["fraction"] * max_amp) / 2
    D = max_amp - A

    # For creating wave
    time = modulation_data["total_time"] / 1000
    start = 0
    stop = time
    x = np.linspace(start, stop, int(time * 1000 / modulation_data["dis"]))

    # Create amplitude list
    amplitude_list = []
    for i in range(len(x)):
        amplitude_list.append(
            (int)(A * np.sin(B * (x[i] - modulation_data["phase_change"])) + D)
        )

    return process_amplitude_list(
        amplitude_list,
        modulation_data["coord_list"],
        modulation_data["freq"],
        modulation_data["path_like"],
        modulation_data["is_static"],
    )


def generate_pattern(staticPattern: bool, pathPattern: bool, waveform: str) -> list:
    coord_list = []
    all_waves = []
    if staticPattern is True:
        n_actuators = random.choice(config.static_actuators_no)
    else:
        n_actuators = random.choice(config.dynamic_actuators_no)

    if pathPattern is True:
        if len(coord_list) == 0:
            coord_list = [
                (
                    random.randint(1, config.grid_width),
                    random.randint(1, config.grid_height),
                )
            ]

        # TODO add stridded pathLike patterns

        # Select which actuators are active
        for _ in range(n_actuators):
            last_w = coord_list[-1:][0][0]
            last_h = coord_list[-1:][0][1]

            # print("H:" + str(last_h) + " W:" + str(last_w))

            if last_h == config.grid_height:
                # new_h = random.choice([random.randint(last_h - 1, last_h), 1])
                new_h = random.randint(last_h - 1, last_h)
            elif last_h == 1:
                # new_h = random.choice([random.randint(last_h, last_h + 1), 6])
                new_h = random.randint(last_h, last_h + 1)
            else:
                new_h = random.randint(last_h - 1, last_h + 1)

            if last_w == config.grid_width:
                new_w = random.choice([random.randint(last_w - 1, last_w), 1])
                # Uncomment next line and comment out the previous line to disable periodic generation
                # new_w = random.randint(last_w - 1, last_w)
            elif last_w == 1:
                new_w = random.choice([random.randint(last_w, last_w + 1), 4])
                # new_w = random.randint(last_w, last_w + 1)
            else:
                new_w = random.randint(last_w - 1, last_w + 1)

            coord_list.append((new_w, new_h))
    else:
        if staticPattern is True:
            patterns_no = 1
        else:
            patterns_no = config.patterns_no

        for _ in range(patterns_no):
            coord_list = [
                (
                    random.randint(1, config.grid_width),
                    random.randint(1, config.grid_height),
                )
                for _ in range(n_actuators)
            ]

    """
    total_time: total time of sinus in ms, e.g. 392
    modulation: modulation of wave in Hz, e.g. 30
    fraction: fraction of the max amplitude of the motors to be the minimum of the wave, default 0.5
    phi: phase change, e.g. 0.4*(1 / modulation)
    dis: discretization rate, default for 92 time waves is 6, default for 392 time waves is 12
    coord_list: list of coordinates, e.g. [12, 13, 14, 15]
    pho_freq: frequency of phoneme, e.g. 300
    dynamic: generate siple or dynamic pattern
    pathLike: generate pathLike or completely random pattern

    returns: dict representing a pattern
    """
    modulation_input = {
        "total_time": random.choice(config.total_time),
        "modulation": random.choice(config.modulation),
        "fraction": config.fraction,
        "phase_change": random.choice(config.phase_change),
        "dis": config.discretization_rate,
        "coord_list": coord_list,
        "freq": random.choice(config.frequency),
        "path_like": pathPattern,
        "is_static": staticPattern,
    }

    if waveform == "hanning":
        all_waves += hanning_modulation(modulation_input)
    elif waveform == "block":
        all_waves += block_modulation(modulation_input)
    elif waveform == "sawtooth":
        all_waves += sawtooth_modulation(modulation_input)
    else:
        all_waves += sin_modulation(modulation_input)

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
        required=False,
    )

    parser.add_argument(
        "--hanning",
        default=False,
        action="store_true",
        help="generate patterns with hann function modulation",
        required=False,
    )

    parser.add_argument(
        "--block",
        default=False,
        action="store_true",
        help="generate patterns with block modulation",
        required=False,
    )

    parser.add_argument(
        "--sawtooth",
        default=False,
        action="store_true",
        help="generate patterns with block modulation",
        required=False,
    )

    parser.add_argument(
        "--numpy",
        default=False,
        action="store_true",
        help="export patterns to numpy binary format",
        required=False,
    )

    return parser


if __name__ == "__main__":
    parser = initArgsParser()
    args = parser.parse_args()

    if args.pathLike is True and args.static is True:
        print(
            "Warning: Static patterns cannot be path-like. Generating static patterns..."
        )

    # If more than one waveform is passed
    if sum([args.hanning, args.block, args.sawtooth]) > 1:
        print("Error: only one waveform can be specified at the time. Quitting...")
        exit(1)

    wavetype = ""
    if args.hanning is True:
        wavetype = "hanning"
    elif args.block is True:
        wavetype = "block"
    elif args.sawtooth is True:
        wavetype = "sawtooth"
    else:
        wavetype = "sin"

    for n in range(args.n):
        all_waves = generate_pattern(
            staticPattern=args.static, waveform=wavetype, pathPattern=args.pathLike
        )

        # TODO don't generate gifs from json
        json_pattern = {"pattern": all_waves}
        with open("p_" + str(n+1) + ".json", "w") as f:
            json.dump(json_pattern, f)

        if args.jsonOnly is False:
            with open("p_" + str(n+1) + ".json", "r") as f:
                json_pattern = json.load(f)

            iters = [iteration["iteration"] for iteration in json_pattern["pattern"]]
            grids = [
                [[[0, 0, 0] for _ in range(0, 4)] for _ in range(0, 6)]
                for _ in range(0, len(iters))
            ]

            for i, iteration in enumerate(iters):
                for iter in iteration:
                    col_coord = int(iter["coord"][0])
                    row_coord = int(iter["coord"][1])
                    amp = iter["amplitude"]
                    grids[i][row_coord - 1][col_coord - 1] = [amp, amp, amp]

            gifutils.save_frames_as_gif(
                gifutils.frames_from_lists(grids), "gifs", "p_" + str(n+1)
            )

            if args.numpy is True:
                np.save(f"p_{n+1}", grids)