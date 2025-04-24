# Mind of stairs

<video width="640" height="480" controls>
  <source src="/video/Maya_Final_Project.mp4" type="video/mp4">
</video>

## Introduction

The origin of ideas is a mystery that we have yet to unravel. Throughout the day, our
minds can generate hundreds of ideas and thoughts, but only a few convince us to take
action and bring them to life. In this project, my goal was to explore the concept of an
impossible staircase and imagine ideas as small entities bouncing around the mind
randomly. This is my interpretation of how ideas interact in my mind and how, in
order to perceive them, we need to observe them from a specific angle to find the
necessary sense and coherence, just like with an impossible staircase.

## Project idea

Create a head structure where the impossible staircases represent the complexity and
paradoxes of thought, while bouncing balls symbolize fleeting ideas, thoughts, or
inspiration.

## Modelling

For the modeling phase, I focused on creating a voxelized head model. Initially, I wrote
a Python script to process the head's OBJ file. The script extracted mesh data, created
a bounding box, and evaluated whether each cube within it was inside or outside the
head mesh. Cubes inside the mesh formed a Lego-style representation of the head.
To determine intersections, I used Maya's ray tracing formula, which counts
intersections to pinpoint the location of a point. While the script worked, the smallest
cubes I could generate were 0.5 cm³, resulting in a relatively coarse mesh. Below are
some examples of the head generated using this approach.

To improve the results, I switched to Houdini, which offered better tools for managing
the large number of cubes needed for a detailed voxelized head. Houdini allowed me to
create a more refined and visually appealing final model, as shown in the image below.

## 3. Animation 
Animating the main ball involved careful planning to ensure smooth transitions between
its jumps on the steps and its movement across flat surfaces. Using the animation editor,
I fine-tuned the tangents of the motion graph to create a natural flow. Additionally, I
applied stretch and squash effects by scaling the ball, adding dynamic and lifelike
qualities to both the primary ball and the secondary balls.

## 4. Rendering

During the rendering stage, different colors and textures were tested to highlight the
key elements of the project. The head is the element more relevant in the scene, so I
focus in experiment with differente textures and colors. These are a couple examples of
colors that I use to test.

## 5. Challenges 

Before starting this project, the only skill I had was programming in Python. Everything
else was completely new to me, from learning Maya and its script editor to rendering,
assigning textures, working with lights and editing. Below, I’ve listed some of the main
challenges I faced while working on this project.

1. Creating a Lego-style voxel head began with a Python script to process the OBJ file,
identify mesh intersections, and generate cubes inside the mesh using Maya's ray
tracing formula. However, the 0.5 cm³ cube limit made the model coarse. Switching to
Houdini resolved this by enabling higher precision and better organization, resulting
in a more refined and appealing head.

2. Selecting the right head model was essential, as its topology influenced the design of
the stairs and the available space for placement. Testing various models helped
finalize one that offered the best balance of detail and compatibility for voxelization.

3. Designing stairs required careful consideration of angles and composition to align with
the head model. Through multiple trials with different stair designs, I achieved a setup
that fit the intended aesthetic and spatial constraints.

4. Animating the ball posed challenges in ensuring smooth transitions between steps and
flat surfaces. Adjustments to motion tangents and stretch-and-squash effects added
realism to the movement.

5. Color space mismatches during rendering required corrections in DaVinci Resolve to
achieve the desired visual consistency.