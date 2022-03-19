import argparse
# Modyfying some of these values may cause the generator to crash

modulation: list = [60]
total_time: list = [92, 392]
fraction: float = 0.5
phase_change: list = [0, 0.2, 0.4, 0.6, 0.8]

# Decreasing discretization rate increases the number of detail and vice versa
discretization_rate: int = 8

# Number of actuators active during the execution of a pattern
static_actuators_no: list = [x for x in range(1,9)]
dynamic_actuators_no: list = [x for x in range(2,17)]

# Grid dimensions
# Gif conversion utility may require further adjustments if you want to change that
grid_height: int = 6
grid_width: int = 4

# Frequency
frequency: list = [300]

# Number of iterations for dynamic pattern
patterns_no: list = [x for x in range(2, 8)]

# Maximal amplitude
max_amp: int = 255

# List of allowed maximum amplitudes
amplitudes: list = [100, 255]


def initArgsParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate dynamic patterns")
    parser.add_argument(
        "-n", type=int, nargs='?', help="number of patterns to generate", required=True
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
        help="export patterns to a numpy binary",
        required=False,
    )

    parser.add_argument(
        "--stridden",
        default=False,
        action="store_true",
        help="generate stridden pathLike patterns",
        required=False,
    )

    return parser