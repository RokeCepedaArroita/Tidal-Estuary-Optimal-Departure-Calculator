import numpy as np
import matplotlib.pyplot as plt
from kayak import *
from currents import *

# Configuration
tidal_amplitude = 4.8           # m, difference between maximum and minimum tide height
river_max_current_speed = 0.91  # km/h speed of river at the end, tapered linearly from source (max speed) to sea (0 speed)
kayak_speed = 4.7               # km/h, speed of kayak relative to water, slower than 5.5 to account for pauses (prop cleaning)
river_length = 7.7              # km, one way length of river


# Hypersimulation
tidal_amplitudes = [0, 1, 2, 3, 4, 5]
colors = ['#ADD8E6', '#8AACD3', '#6781C1', '#4556AF', '#222B9D', '#00008B']

for tidal_amplitude, color in zip(tidal_amplitudes, colors):

    # Intermediate parameters
    max_tidal_current_speed_kmh = max_tidal_current_speed(tidal_amplitude)

    # Travel times
    start_times = np.linspace(-3,0,200)
    travel_times = []
    from tqdm import tqdm
    for start_time in tqdm(start_times):
        # Simulate trip
        travel_time, travel_distance, times, distances, tidal_currents, river_currents, effective_speeds = \
            simulate_trip(start_time, max_tidal_current_speed_kmh, river_max_current_speed, river_length, kayak_speed, plot=False)
        # Record travel time
        travel_times.append(travel_time)


    # Plot results

    if tidal_amplitude > 0:
        plt.plot(start_times, travel_times, label=f'{tidal_amplitude} m → Start {hours_to_hm_str(start_times[np.argmin(travel_times)])}  (trip {hours_to_hm_str(np.min(travel_times))})', color=color)
        plt.plot(start_times[np.argmin(travel_times)], np.min(travel_times), marker=11, color=color)
    else:
        plt.plot(start_times, travel_times, label=f'{tidal_amplitude} m → Start N/A           (trip {hours_to_hm_str(np.min(travel_times))})', color=color)

plt.xlabel('Starting time (hours wrt high tide)')
plt.ylabel('Total travel time (h)')
plt.ylim([2.4,3.8])
plt.xlim([np.min(start_times),np.max(start_times)])
plt.grid()
plt.legend(loc='upper left')
plt.show()

print(travel_time, travel_distance)





# # Time range for plotting
# time = np.linspace(-6, 6, 1000)  # 12 hours before and after the peak
#
# # Query the functions for tide height and tidal current speed
# tide_heights = tide_height(time, peak_height=tidal_amplitude/2.)
# tidal_currents = tidal_current_speed(time, max_tidal_current_speed=max_tidal_current_speed)
#
# # Plotting
# fig, ax1 = plt.subplots()
# plt.grid()
# color = 'tab:blue'
# ax1.set_xlabel('Time (hours)')
# ax1.set_ylabel('Tide Height (m)', color=color)
# ax1.plot(time, tide_heights, color=color)
# ax1.tick_params(axis='y', labelcolor=color)
#
# ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
# color = 'tab:red'
# ax2.set_ylabel('Tidal Current Speed (km/h)', color=color)
# ax2.plot(time, tidal_currents, color=color)
# ax2.tick_params(axis='y', labelcolor=color)
#
# fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.title('Tide Height and Tidal Current Speed Over Time')
# plt.show()
