import displayio
import terminalio
from adafruit_gizmo import tft_gizmo
import random

##### Globals #####

attach_prob = .5  # probability of attachment

###################

def gen_cells(start_x, start_y):
    """ generate addresses of surrounding cells.

    Returns:
        iterable list of cell address pairs
    """
    rv = []
    
    # upper left
    cp_x = start_x - 1
    cp_y = start_y - 1
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])
        
    
    # left
    cp_x = start_x - 1
    cp_y = start_y
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])

    # lower left
    cp_x = start_x - 1
    cp_y = start_y + 1
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])

    # bottom
    cp_x = start_x
    cp_y = start_y + 1
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])

    # lower right
    cp_x = start_x + 1
    cp_y = start_y + 1
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])

    # right
    cp_x = start_x + 1
    cp_y = start_y
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])

    # right
    cp_x = start_x + 1
    cp_y = start_y - 1
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])

    # above
    cp_x = start_x
    cp_y = start_y - 1
    if cp_x >= 0 and cp_y >= 0 and cp_x < display.width and cp_y < display.height:
        rv.append([cp_x, cp_y])

    if 0 == len(rv):
        # No points to add
        rv.append([-1,-1])

    return(rv)

##### main #####

# display = board.DISPLAY
display = tft_gizmo.TFT_Gizmo()

# Display context
splash = displayio.Group(max_size=10)
display.show(splash)

# Create a bitmap with two colors
color_bitmap = displayio.Bitmap(display.width, display.height, 3)

# Create a two color palette
color_palette = displayio.Palette(3)
color_palette[0] = 0x000000
color_palette[1] = 0x0000ff    # blue (old activations)
color_palette[2] = 0xff0000    # red (most recent activiation)

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.show(group)

# Make the whole field black
for x in range(0,display.width):
    for y in range(0,display.height):
        color_bitmap[x,y] = 0

# Build the fractal

# Draw a random pixel
rand_x = random.randint(0, (display.width - 1))
rand_y = random.randint(0, (display.height - 1))
color_bitmap[rand_x, rand_y] = 2

while True:
    for x in range(0,display.width):
        for y in range(0,display.height):
            if 2 == color_bitmap[x,y]:
                # Can start here
                color_bitmap[x, y] = 1
                for new_point in gen_cells(x, y):
                    new_x = new_point[0]
                    new_y = new_point[1]
                    if new_x >= 0 and new_y >= 0:
                        if 0 == color_bitmap[new_x, new_y]:
                            if attach_prob >= random.random():
                                # turn on a new pixel
                                color_bitmap[new_x, new_y] = 2

