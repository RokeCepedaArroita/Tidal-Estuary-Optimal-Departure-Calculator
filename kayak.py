import numpy as np

def simulate_trip(start_time, max_tidal_current_speed, river_max_current_speed, river_length, kayak_speed, verbose=False, plot=False):

    from currents import tidal_current_speed, river_current_speed

    # Simulation step size
    delta_time = 2/60/60 # h, 2 s intervals (2 m uncertainty)

    # Start time and distance
    time = start_time   # hours relative to high tide, which is time=0
    distance = 0        # km
    travel_distance = 0 # km, cumulative distance

    # Store variables
    distances = []
    times = []
    tidal_currents   = []
    river_currents   = []
    effective_speeds = []

    # Upriver leg
    while distance < river_length:

        # For each segment, calculate time elapsed and distance covered
        tidal_current = tidal_current_speed(time, max_tidal_current_speed)
        river_current = river_current_speed(distance, river_max_current_speed, river_length)
        effective_speed = kayak_speed + tidal_current + river_current

        if verbose:
            print(f't = {time:.1f} h, d = {distance:.1f} km, v_t = {tidal_current:.1f} km/h, v_r = {river_current:.1f} km/h, v_e = {effective_speed:.1f} km/h')

        # Store variables
        distances.append(distance)
        times.append(time)
        tidal_currents.append(tidal_current)
        river_currents.append(river_current)
        effective_speeds.append(effective_speed)

        # Compute distance travelled and advance time
        time = time + delta_time
        distance = distance + effective_speed*delta_time
        travel_distance = travel_distance + np.abs(effective_speed*delta_time)


    # Downriver leg
    while distance > 0:

        # For each segment, calculate time elapsed and distance covered
        tidal_current = tidal_current_speed(time, max_tidal_current_speed)
        river_current = river_current_speed(distance, river_max_current_speed, river_length)
        effective_speed = -kayak_speed + tidal_current + river_current

        if verbose:
            print(f't = {time:.1f} h, d = {distance:.1f} km, v_t = {tidal_current:.1f} km/h, v_r = {river_current:.1f} km/h, v_e = {effective_speed:.1f} km/h')

        # Store variables
        distances.append(distance)
        times.append(time)
        tidal_currents.append(tidal_current)
        river_currents.append(river_current)
        effective_speeds.append(effective_speed)

        # Compute distance travelled and advance time
        time = time + delta_time
        distance = distance + effective_speed*delta_time
        travel_distance = travel_distance + np.abs(effective_speed*delta_time)

    travel_time = time - start_time

    # Flip negatives in effective speed and return only absolute effective speed
    effective_speeds = np.abs(effective_speeds)

    if plot:

        import matplotlib.pyplot as plt

        # Plotting
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Distance (km)', color='b')
        ax1.plot(times, distances, color='b')
        ax1.tick_params(axis='y', labelcolor='b')

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel('Tidal Current Speed (km/h)', color='r')
        ax2.plot(times, np.zeros(np.shape(times)), 'k') # set the zero speed mark
        ax2.plot(times, tidal_currents,   'r--', label='Tidal current')
        ax2.plot(times, river_currents,   'r:' , label='River current')
        ax2.plot(times, effective_speeds, 'r-' , label='Effective speed')
        ax2.tick_params(axis='y', labelcolor='r')
        ax2.grid(True, which='both', axis='y', color='gray', linestyle='--', linewidth=0.5)


        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title('Simulated Estuary Trip')
        plt.legend()
        plt.xlim([np.min(times), np.max(times)])
        plt.show()

    return travel_time, travel_distance, times, distances, tidal_currents, river_currents, effective_speeds




def hours_to_hm_str(hours):
    ''' Convert hours to a string format "Hh Mmin"
    where H is hours and M is minutes, with leading zeros for minutes. '''
    # Absolute value to handle negative inputs
    hours_abs = abs(hours)
    # Extract whole hours
    h = int(hours_abs)
    # Extract remaining minutes, with leading zeros if less than 10
    m = int((hours_abs - h) * 60)
    return f"{h}h {m:02d}min"
