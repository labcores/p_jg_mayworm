# -*- coding: utf-8 -*-

import numpy as np

#==============================================================================#
#--- Geographical Calculations ------------------------------------------------#
#==============================================================================#

def calculate_angle(start, dest):
    """
    Calculates the bearing between two points.

    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """
    d_lon = (dest[1] - start[1])

    y = np.sin(d_lon) * np.cos(dest[0])
    x = np.cos(start[0]) * np.sin(dest[0]) - np.sin(start[0]) \
            * np.cos(dest[0]) * np.cos(d_lon)

    angle = (np.arctan2(y, x) + 2*np.pi)%(2*np.pi)
    return (np.rad2deg(angle) + 360) % 360

#------------------------------------------------------------------------------#

def calculate_next_point(start, dist, angle):
    R = 6378100.0 #Radius of the Earth.

    lat1 = start[0] * (np.pi/180)  #Current lat point converted to radians
    lon1 = start[1] * (np.pi/180)  #Current long point converted to radians
    angle = angle * (np.pi/180)

    lat2 = np.arcsin(np.sin(lat1) * np.cos(dist/R) + np.cos(lat1) * np.sin(dist/R) * np.cos(angle))
    lon2 = lon1 + np.arctan2(np.sin(angle) * np.sin(dist/R) * np.cos(lat1), np.cos(dist/R) - np.sin(lat1) * np.sin(lat2))

    lat2 = lat2 * (180/np.pi)
    lon2 = lon2 * (180/np.pi)
    return (lat2, lon2)

#------------------------------------------------------------------------------#

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = np.radians(lat2-lat1)
    dlon = np.radians(lon2-lon1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) \
        * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = radius * c

    return d

#------------------------------------------------------------------------------#

#Printing inverted coordinates to paste in google maps - google style bitch!
def inverted_coords(coord=(), path=[]):
    inverted_coords = []
    if not path:
        lat, lon = coord
        return (lon, lat)
    if path:
        for point in path:
            inverted_coords.append((point[1], point[0]))
        return inverted_coords

#==============================================================================#

