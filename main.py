import math
import random
import pygame
import colorsys

# global const variables
looping = True
mouse_dragging = False
ui_width = 600
ui_height = 500
sand_size = 5
sand_hue = 0.01
sand_spawn_chunk_size = 5
columnCount = int(ui_width / sand_size)
rowCount = int(ui_height / sand_size)

# 2D Matrix grid style to check each state of the "game"
grid = [[0.0 for _ in range(rowCount)] for _ in range(columnCount)]
nextGrid = grid

# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((ui_width, ui_height))
pygame.display.set_caption('Falling Sand Sim')

Icon = pygame.image.load('sand.png')
pygame.display.set_icon(Icon)

# Loop event to update sand
pygame.time.set_timer(pygame.USEREVENT, 20)

# Sand sound effect when falling
pygame.mixer.pre_init()
pygame.mixer.Channel(0).set_volume(0.01)
sand_fall_sound = pygame.mixer.Sound("fall.mp3")


def within_rows(x):
    return 0 <= x <= rowCount - 1


def within_cols(x):
    return 0 <= x <= columnCount - 1


def update_sand():
    global grid, nextGrid, sand_hue

    # Draw the sand
    for i in range(0, columnCount):
        for j in range(0, rowCount):
            if grid[i][j] > 0:
                r,g,b = colorsys.hsv_to_rgb(grid[i][j], 1, 1)
                r,g,b = round(r * 255), round(g * 255), round(b * 255)
                add_sand(i, j, (r,g,b))
            else:
                add_sand(i, j, 'black')

    nextGrid = [[0 for _ in range(rowCount)] for _ in range(columnCount)]

    # Check every cell
    for i in range(0, columnCount):
        for j in range(0, rowCount):
            state = grid[i][j]
            # if detected sand which is signalled by having a state above zero then go to the logic
            # for sand to fall.
            if state > 0:
                # first check if I can access the state below of the sand, meaning, if the sand is
                # already at the floor then I cannot go further below the grid (will throw an error).
                if j + 1 >= rowCount:
                    nextGrid[i][j] = state
                else:
                    state_below = grid[i][j + 1]

                    # random direction for the sand to fall
                    rand_dir = 1
                    if random.uniform(0,1) > 0.5:
                        rand_dir *=-1

                    # check if random direction selected is valid to place sand
                    state_below_left, state_below_right = -1, -1
                    if within_cols(i - 1):
                        state_below_left = grid[i - 1][j + 1]
                    if within_cols(i + 1):
                        state_below_right = grid[i + 1][j + 1]

                    # if in the current state of the grid there is no sand below then go below
                    if state_below == 0 and j < rowCount - 1:
                        nextGrid[i][j + 1] = state

                    # else if there is already sand below in current state then try to make sand fall to
                    # the right or left randomly
                    elif state_below_left == 0 or state_below_right == 0:
                        if rand_dir == 1:
                            if state_below_left == 0:
                                nextGrid[i - 1][j] = state
                            elif state_below_right == 0:
                                nextGrid[i + 1][j] = state
                        else:
                            if state_below_right == 0:
                                nextGrid[i + 1][j] = state
                            elif state_below_left == 0:
                                nextGrid[i - 1][j] = state

                    # if sand cannot go below or to the right or left then stay in place
                    # (redundant condition but defined here just for safety)
                    else:
                        nextGrid[i][j] = state

    # update current grid state with the next "epoch"
    grid = nextGrid


def add_sand(x, y, color):
    pygame.draw.rect(surface, color, pygame.Rect(x * sand_size, y * sand_size, sand_size, sand_size))


def clear_sand():
    global grid
    grid = [[0.0 for _ in range(columnCount)] for _ in range(rowCount)]


def update_hue():
    global sand_hue
    if sand_hue >= 1:
        sand_hue = 0.1
    else:
        sand_hue += 0.001


def update_grid(pos):
    global sand_spawn_chunk_size
    mouse_x = int(pos[0] / sand_size)
    mouse_y = int(pos[1] / sand_size)

    # create chunk of sand to fall by having a matrix around the mouse click position
    # be filled and assigned to the current grid.
    matrix_middle = math.floor(sand_spawn_chunk_size / 2)
    for i in range(-matrix_middle, matrix_middle + 1):
        for j in range(-matrix_middle, matrix_middle + 1):
            if random.uniform(0,1) < 0.75:
                col = mouse_x + i
                row = mouse_y + j
                if within_cols(col) and within_rows(row):
                    grid[col][row] = sand_hue


def play_sound():
    global sand_fall_sound
    pygame.mixer.Channel(0).play(sand_fall_sound)


def main():
    global looping, sand_hue, mouse_dragging

    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
                break

            # update sand "motion"
            if event.type == pygame.USEREVENT:
                update_sand()
                update_hue()

            # mouse event: drag
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    play_sound()
                    mouse_dragging = True
                    pos = pygame.mouse.get_pos()
                    update_grid(pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if mouse_dragging:
                    pos = pygame.mouse.get_pos()
                    update_grid(pos)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()











