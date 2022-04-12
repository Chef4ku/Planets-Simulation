import pygame
import math
pygame.init()

# WINDOW SIZE
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")   # TITLE


#WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class Planet:
    AU = 149.6e6 * 1000         # Distance from earth to sun
    G = 6.67428e-11             # Atraction between objects
    SCALE = 250 / AU            # 1 AU = 100 pixels
    TIMESCALE = 3600*24         # 1 day per second


    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.dis_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        pygame.draw.circle(window, self.color, (x, y), self.radius)


# GAME LOOP
def main():
    run = True
    delta_time = pygame.time.Clock()


    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    planets = [sun]

    # When presing esc set run to false.
    while run:
        delta_time.tick(60)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.draw(WIN)

        #WIN.fill(WHITE)
        pygame.display.update()

    pygame.quit()

main()
