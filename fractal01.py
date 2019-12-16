import displayio
import terminalio
from adafruit_gizmo import tft_gizmo
import random

##### Globals #####

attach_prob = .5  # probability of attachment

###################

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

seed_list = []

# Draw a random pixel
rand_x = random.randint(0, display.width)
rand_y = random.randint(0, display.height)
color_bitmap[rand_x, rand_y] = 2
seed_list.append([rand_x, rand_y]) # list of active pixels

def gen_cells(start_x, start_y):
    """ generate addresses of surrounding cells.

    Returns:
        iterable list of cell address pairs
    """
    rv = []
    
    cp_x = start_x - 1
    cp_y = start_y - 1
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])
        
    
    cp_x = start_x - 1
    cp_y = start_y
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])

    cp_x = start_x - 1
    cp_y = start_y + 1
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])

    cp_x = start_x
    cp_y = start_y + 1
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])

    cp_x = start_x + 1
    cp_y = start_y + 1
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])

    cp_x = start_x + 1
    cp_y = start_y
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])

    cp_x = start_x + 1
    cp_y = start_y - 1
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])

    cp_x = start_x
    cp_y = start_y - 1
    if cp_x >= 0 and cp_y >= 0:
        rv.append([cp_x, cp_y])

    if 0 == len(rv):
        # No points to add
        rv.append([-1,-1])

    return(rv)


has_space = True
while has_space:
    add_count = 0
    for cur_point in seed_list:
        # for each tuple in seed_list
        cur_x = cur_point[0]
        cur_y = cur_point[1]
        # Check to see if the point is red
        if 2 == color_bitmap[cur_x, cur_y]:
            color_bitmap[cur_x, cur_y] = 1
            # check the eight cells around the current cell. Can't
            # put a cell next to another cell (except the current one)
            for new_point in gen_cells(cur_x, cur_y):
                new_x = new_point[0]
                new_y = new_point[1]
                if new_x >= 0 and new_y >= 0:
                    add_count += 1
                    if attach_prob >= random.random():
                        # turn on a new pixel
                        color_bitmap[new_x, new_y] = 2
                        # add pixel tuple to seed_list
                        seed_list.append([new_x, new_y])
    if 0 == add_count:
        has_space = False

# No points to add, done
while True:
    pass

