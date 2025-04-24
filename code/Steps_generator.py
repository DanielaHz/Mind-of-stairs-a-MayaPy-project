# Code to generate steps for the impossible staircase.

# --------------------------------------------------------------------------------------------------
# Note: The model of the staircase that I implemented in my head project is quite complex and took a lot of
# experimentation. In the end, I decided to generate the steps programmatically, but the composition
# of the main staircase and the secondary ones was experimental.
# --------------------------------------------------------------------------------------------------

import maya.cmds as cmds

def move_relative(model, position):
    cmds.move( position[0] , position[1], position[2], model, absolute = True)

def make_step(width, height, depth):
    step = cmds.polyCube(width=width, height = height, depth = depth)

def main():
    #create the floor steps 
    step_1 = make_step(10, 1, 3)
    step_2 = make_step(3,1,23 )
    step_3 = make_step(3,1,3)

    #create the other steps
    position_count_z = -1
    position_count_y = 1
    position_x = 0

    for i in range(1,11):
        step = make_step(2, 0.5, 0.5)
        move_relative(step,(position_x, position_count_y,position_count_z))
        position_count_z -= 0.5
        position_count_y += 0.5
        
    step_4 = make_step(3,1,3)

if __name__ == "__main__":
    main()