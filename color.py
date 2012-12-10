import webcolors

# Color conversion functions

def simple_color(css21_color_name):
    """Converts CSS 2.1 color name to less bougie names"""
    d = {'white': 'white',
     'silver': 'white',
     'gray': 'white',
     'black': 'black',
     'red': 'red',
     'maroon': 'red',
     'orange': 'orange',
     'yellow': 'yellow',
     'olive': 'green', # Could be yellow or green...
     'lime': 'green',
     'green': 'green',
     'aqua': 'blue',
     'teal': 'blue',
     'blue': 'blue',
     'navy': 'blue',
     'fuchsia': 'purple',
     'purple': 'purple',
    }
    return d.get(css21_color_name, "NONE")

def color_abbreviation(simple_color_name):
    d = {'white': 'W',
     'black': 'BL',
     'red': 'R',
     'orange': 'O',
     'yellow': 'Y',
     'green': 'G',
     'blue': 'B',
     'purple': 'P',
    }
    return d.get(simple_color_name, "NONE")

# Code snippet from stackoverflow user fraxel with slight modification
# Source: http://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    """Given tuple (r,g,b) returns nearest CSS 2.1 color name"""
    try:
        actual_name = webcolors.rgb_to_name(requested_colour,spec='css21')
        return actual_name
    except ValueError:
        closest_name = closest_colour(requested_colour)
        return closest_name

def get_simple_color_name(requested_colour):
    return simple_color(get_colour_name(requested_colour))
