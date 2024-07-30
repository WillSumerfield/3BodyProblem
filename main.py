import pygame
import sys
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Two Body Problem")
clock = pygame.time.Clock()
FPS = 60

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Physics sim definitions
G = 6.67430
timestep = 1
timestep_sq = timestep*timestep/2.0

# Zoom of the game
zoom = 1.0


# Galactic Bodies
class Body():

    def __init__(self, mass, color, pos, vel):
        self.mass = mass
        self.size = mass/2
        self.color = color
        self.pos = np.array(pos, dtype='float64')
        self.vel = np.array(vel, dtype='float64')
        self.acc = np.zeros(2,   dtype='float64')

bodies = [Body(40, RED, [200, 50], [0, 1]), Body(80, BLUE, [400, 400], [0, 0]), Body(12, GREEN, [600, 400], [0, -2])]
primary = 0

# Main game loop
running = True
while running:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            zoom *= 1+event.y*0.2
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            primary = (primary+1) % len(bodies)                                 

    # Fill the screen with white
    screen.fill(WHITE)

    # Calculate the attraction between the bodies
    for i, body in enumerate(bodies):
        body.acc = np.zeros(2)        

        # For ecah other Body
        for i2, body2 in enumerate(bodies):
            if i == i2:
                continue

            diff = body.pos - body2.pos
            distance = np.linalg.norm(diff)

            # Collisions
            min_dist = body.size + body2.size
            if i > i2 and distance < min_dist:

                if distance == 0:
                    diff[0] = 1e-10
                    diff[1] = 1e-10
                    distance = np.linalg.norm(diff)

                mass_sum = body.mass + body2.mass
                mass_diff = body.mass - body2.mass
                vel_diff = body.vel - body2.vel
                pos_diff = body.pos - body2.pos

                # Find how far back they need to move to be just touching
                a = np.sum(vel_diff*vel_diff)
                b = 2*np.sum(pos_diff*vel_diff)
                c = np.sum(pos_diff*pos_diff) - (min_dist*min_dist)
                t = (-b - np.sqrt(b*b - 4*a*c))/(2*a)

                # Move the bodies back in time a bit to where they just meet
                body.pos += body.vel*t
                body2.pos += body2.vel*t

                # Make the bodies bounce off one another
                bvel = (mass_diff*body.vel + 2*body2.mass*body2.vel) / mass_sum
                body2.vel = (-mass_diff*body2.vel + 2*body.mass*body.vel) / mass_sum
                body.vel = bvel

            d3 = pow(distance, 3)
            body.acc += body.acc + (body2.mass*diff)/d3

        body.acc *= -G

    # Calculate the new positions of each body
    for body in bodies:

        body.pos += body.vel*timestep + body.acc*timestep_sq
        body.vel += body.acc*timestep

    # Draw Bodies
    for body in bodies:
        pos = 400+((body.pos-bodies[primary].pos)*zoom)
        size = body.size*zoom
        pygame.draw.circle(screen, body.color, pos, size)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
