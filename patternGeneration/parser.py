import argparse

# Initialize and return a parser object
def init_argsparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate dynamic patterns")
    parser.add_argument(
        "-n", type=int, nargs='?', help="number of patterns to generate", required=True
    )

    parser.add_argument(
        "--ubjson",
        default=False,
        action="store_true",
        help="additionaly generate ubjson files for future communication with the sleeve",
        required=False,
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