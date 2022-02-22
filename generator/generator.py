from io import UnsupportedOperation
import os, json, sys, string, random
import numpy as np
import moviepy.editor
import scipy.signal

# type of E: 'set' which is a subset of (4,6), e in E, e[0] is '4', e[1] is '6'
# type of D: duration in of the pattern (integer in ms)
# type of G_f: frequency of wave type (integer)
# type of W: string, denoting the wave type

POSSIBLE_WAVEFORMS = ['sin', 'sawtooth', 'block', 'hanning', 'constant']


def staticPattern(E, a, f, d, g_f, w) -> list:
    """
    #TODO: add drawing somewhere

    We say 'extra' is a parameter either a or f.
    We say 'x' is from top view of the grid the x-coordinate
    We say 'y' is from top view of the grid the y-coordinate

    :param E: (array) subset of whole grid. E = E[e_1,e_2,...]. For each e in E: x=e[0], y=e[1]
    :param a: (int: mm) one of all amplitudes. a = a in A
    :param f: (int: Hz) one of all frequencies. f = f in F
    :param d: (int: ms) one of all durations. d = d in D ()
    :param g_f: (int) one of all group frequencies. g_f = g_f in G_f. Also known as 'modulation'
    :param w: (str) one of all wave types. w = w in W
    :return: array: (array) an array representing the pattern in video form. array = array[time][x][y][extra].
             note that array[][][][0] gives the frequency, and array[][][][1] gives the amplitude.
             """

    # initial values
    max_amp = 250
    delta_t = 10
    discretization = d // delta_t
    array = np.zeros(shape=(discretization,4,6,2)) #maybe useful to make this a custom class

    if w == 'constant':
        for timestep in range(discretization):
            for e in E:
                array[timestep][e[0]-1][e[1]-1][0] = f
                array[timestep][e[0]-1][e[1]-1][1] = a

    elif w == 'sin':
        # Note that we assume a sine wave y = A sin(B(x-phi))+D

        # Computed from input
        B = 2*np.pi*g_f
        A = (max_amp - 0.5*max_amp)/2   # assuming a sin wave with 0.5*max_amp amplitude
        D = max_amp - A                 # wave between max_amp and max_amp/2

        # For creating wave
        start = 0
        stop = d
        x = np.linspace(start, stop, discretization)

        #create amplitude list
        phi = 0
        amplitude_list = []
        for i in range(len(x)):
            amplitude_list.append((int) (A*np.sin(B*(x[i] - phi)) + D))

        for timestep in range(discretization):
            for e in E:
                array[timestep][e[0]-1][e[1]-1][0] = f
                array[timestep][e[0]-1][e[1]-1][1] = amplitude_list[timestep]

    elif w == 'sawtooth':
        # TODO: add explanation of theoretic function from signal.sawtooth

        # Computed from input
        B = 2*np.pi*g_f

        # for creating a wave
        start = 0
        stop = d
        x = np.linspace(start, stop, discretization)

        # Create amplitude list
        phi = 0
        amplitude_list = []
        for i in range(len(x)):
            amplitude_list.append((int) ((max_amp*scipy.signal.sawtooth(B * (x[i] - phi)) + max_amp)/2))

        for timestep in range(discretization):
            for e in E:
                array[timestep][e[0]-1][e[1]-1][0] = f
                array[timestep][e[0]-1][e[1]-1][1] = amplitude_list[timestep]

    elif w == 'hanning':
        # Note that we assume a hanning window y = 0.5(1 - cos(2pin/N)), 0 <= n <= N  # noqa: E501
        # This function is built into numpy as hanning(discretization_rate).

        #create amplitude list
        amplitude_list = max_amp * np.hanning(discretization) #hanning window

        for timestep in range(discretization):
            for e in E:
                array[timestep][e[0]-1][e[1]-1][0] = f
                array[timestep][e[0]-1][e[1]-1][1] = amplitude_list[timestep]

    elif w == 'block':
        # Note that we assume a block function y = 1 if 0 <= x < period, -1 if period < x < 2*period

        # can be calculated from input
        period = 1 / g_f

        # for creating wave
        start = 0
        stop = d
        x = np.linspace(start, stop, discretization)

        #create amplitude list
        phi = 0
        amplitude_list = []
        for i in range(len(x)):
            if x[i] % 2*period < period: # if 0 <= x < period
                sign = 1
                amplitude_list.append((int) (a * sign))
            else:                         # period <= x < 2*period
                sign = -1
                amplitude_list.append((int) (a * sign))
        for timestep in range(discretization):
            for e in E:
                array[timestep][e[0]-1][e[1]-1][0] = f
                array[timestep][e[0]-1][e[1]-1][1] = amplitude_list[timestep]
    else:
        print("error: wave type unknown")
        sys.exit(1)

    return array


"""
:param name: (str) name of the pattern
:param grid_width: (int) width of the grid
:param grid_height: (int) height of the grid
:param actuators_no: (tuple) -> (lower, upper) bound on amounts of actuators enabled. 
:param amplitudes: (list) list of amplitudes
:param frequencies: (list) list of frequencies
:param modulations: (list) list of modulation frequencies
:param durations: (list) list of durations
:param waveforms: (list) waveform options, pick one or more from from ['sin', 'sawtooth', 'block', 'hanning', 'constant']
:return: tuple of (name: str, pattern: list). Pattern representing the pattern in video form. pattern = pattern[time][x][y][extra].
         note that pattern[][][][0] gives the frequency, and pattern[][][][1] gives the amplitude.
"""
def generateRandomPattern(
    name: str,
    grid_width: int = 4,
    grid_height: int = 6,
    actuators_no: tuple = (1, 8),
    amplitudes: list = [100, 255],
    frequencies: list = [300],
    modulations: list = [8],
    durations: list = [92, 392],
    waveforms: list = POSSIBLE_WAVEFORMS) -> tuple:

    actuators = random.randint(actuators_no[0], actuators_no[1])
    amplitude = random.choice(amplitudes)
    frequency = random.choice(frequencies)
    modulation = random.choice(modulations)
    duration = random.choice(durations)
    waveform = random.choice(waveforms)
    waveform = random.choice(POSSIBLE_WAVEFORMS)

    enabled_actuators = [(random.randint(1,grid_width), random.randint(1,grid_height)) for _ in range (actuators)]

    return (name, staticPattern(enabled_actuators, amplitude, frequency, duration, modulation, waveform))


"""
:param name: (str) name of the pattern
:param grid: np.ndarray representing the pattern in video form. gird = grid[time][x][y][extra].
         note that grid[][][][0] gives the frequency, and grid[][][][1] gives the amplitude.
:param grid_width: (int) width of the grid
:param grid_height: (int) height of the grid
:param channel_red: (str) amplitude or frequency
:param channel_green: (str) amplitude or frequency
:param channel_blue: (str) amplitude or frequency
"""
def generateGIF(
    name: string,
    grid: np.ndarray,
    grid_width: int = 4,
    grid_height: int = 6,
    channel_red: str = "amplitude",
    channel_green: str = "amplitude",
    channel_blue: str = "amplitude") -> None:

    grids = [[[[255, 255, 255] for _ in range(grid_width)] for _ in range(grid_height)] for _ in range(len(grid))]

    for index, _ in np.ndenumerate(grid):
        # index:
        # (i, j, k, l) where:
        frame = grid[index[0]]

        for column_id, column in enumerate(frame):
            for row_id, row in enumerate(column):
                if channel_red == "frequency" or channel_green == "frequency" or channel_blue == "frequency":
                    raise UnsupportedOperation("frequency channel not supported yet")
                amp = frame[column_id][row_id][1]
                red = 255 - amp
                green = 255 - amp
                blue = 255 - amp
                grids[index[0]][row_id][column_id] = [red, green, blue]

    save_frames_as_gif(frames_from_lists(grids), 'gifs', name)


"""Saves a list of frames as a gif to the given output directory."""
def save_frames_as_gif(frames: np.ndarray, output_dir: str, gif_name: str, fps: int = 10) -> None:

    # If the output dir does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the gif file
    clip = moviepy.editor.ImageSequenceClip(list(frames), fps=fps)
    clip.write_gif(os.path.join(output_dir, gif_name +  ".gif"), fps=fps)


def frames_from_lists(lists: list) -> np.ndarray:
    """Converts a list of arrays into a list of frames."""
    return [np.array(_list, dtype=np.uint8) for _list in lists]


if __name__ == "__main__":
    iters = [iteration['iteration'] for iteration in json.loads(sys.argv[1])['pattern']]
    grids = [[[[255, 255, 255] for _ in range(0,4)] for _ in range(0,6)] for _ in range(0,len(iters))]

    for i, iteration in enumerate(iters):
        col_coord = int(str(iteration[0]['coord'])[0])
        row_coord = int(str(iteration[0]['coord'])[1])
        amp = iteration[0]['amplitude']
        grids[i][row_coord-1][col_coord-1] = [255-amp,255-amp, 255-amp]

    save_frames_as_gif(frames_from_lists(grids), 'gifs', sys.argv[1].split('.')[0])