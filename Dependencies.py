#Contains functions for main

#Remaps pixel values to the display
def remap(value, old_min, old_max, new_min, new_max):
    return (value - old_min) / (old_max - old_min) * (new_max - new_min) + new_min

