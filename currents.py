import numpy as np


def max_tidal_current_speed(tidal_amplitude):
    ''' Scale the tidal current  '''
    max_current_speed = 1.70*(tidal_amplitude/2.1)
    return max_current_speed


def tide_height(time, peak_height):
    ''' Calculate the tide height at a given time, where t=0 hours
    corresponds to the highest tide, and peak_height and tide_height
    are defined as height above the mean level. '''

    period = 12+50/60 # 12-hour 50 minute period standard
    tide_height = peak_height * np.cos(2 * np.pi * time / period)

    return tide_height


def tidal_current_speed(time, max_tidal_current_speed):
    ''' Calculate the tidal current speed at a given time, where t=0 hours
    corresponds to the highest tide and the tidal current speed is
    positive towards land and negative towards the sea '''

    period = 12+50/60 # 12-hour 50 minute period standard
    tidal_current_speed = -max_tidal_current_speed * np.sin(2 * np.pi * time / period)

    return tidal_current_speed


def river_current_speed(distance, river_max_current_speed, river_length):
    '''Calculate the river current speed at a given time. This current reduces
    closer to the sea as the cross sectional area of the river increases. This
    effect is approximated as a linear decrease in speed from the source
    (speed = river_max_current_speed km/h) to the sea (speed = 0). The distance is
    given in the same units as the river_length, and it is zero at the starting
    point. Current speed is positive towards land and negative towards the sea
    (always negative in this case) '''

    river_current = -river_max_current_speed*(distance/river_length)

    return river_current
