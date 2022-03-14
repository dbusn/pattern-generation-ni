import random

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