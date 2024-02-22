from optimal_departure import max_tidal_current_speed, river_max_current_speed, river_length, kayak_speed, max_tidal_current_speed
import matplotlib.pyplot as plt
from kayak import *
from currents import *



travel_time, travel_distance, times, distances, tidal_currents, river_currents, effective_speeds = \
    simulate_trip(start_time, max_tidal_current_speed, river_max_current_speed, river_length, kayak_speed)
