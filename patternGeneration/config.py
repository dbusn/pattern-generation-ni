# BEWARE Modyfying some of these values may cause the generator to crash

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
patterns_no: int = 8

# Maximal amplitude
max_amp: int = 255

# List of allowed maximum amplitudes
amplitudes: list = [100, 255]