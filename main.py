import pygame
import math
pygame.init()

# WINDOW SIZE
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")   # TITLE


WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

class Planet:
    AU = 149.6e6 * 1000         # Distance from earth to sun
    G = 6.67428e-11             # Atraction between objects
    ZOOM = 200 / AU             # 1 AU = 100 pixels
    TIMESCALE = 3600*24         # 1 day per second


    def __init__(self, x, y, radius, color, mass, initial_velocity, is_sun = False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass        # in KiloGrams

        self.orbit = []
        self.is_sun = is_sun
        self.dis_to_sun = 0
        self.x_vel = 0
        self.y_vel = initial_velocity

    def draw(self, window):
        x = self.x * self.ZOOM + WIDTH / 2
        y = self.y * self.ZOOM + HEIGHT / 2

        pygame.draw.circle(window, self.color, (x, y), self.radius)

    def attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.is_sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet: 
                continue
            force_x, force_y = self.attraction(planet)
            total_force_x += force_x
            total_force_y += force_y
        
        # a = f / m
        self.x_vel += total_force_x / self.mass * self.TIMESCALE
        self.y_vel += total_force_y / self.mass * self.TIMESCALE

        self.x += self.x_vel * self.TIMESCALE
        self.y += self.y_vel * self.TIMESCALE
        self.orbit.append((self.x, self.y))


def main():
    run = True
    delta_time = pygame.time.Clock()


    # Creating planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 0, True)
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, 29.783 * 1000)
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, 24.077 * 1000)
    mercury = Planet(-0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, 47.4 * 1000)
    venus = Planet(-0.723 * Planet.AU, 0, 13, WHITE, 4.8685 * 10**24, 35.02 * 1000)

    planets = [sun, earth, mars, mercury, venus]


    # GAME LOOP
    while run:
        delta_time.tick(60)
        WIN.fill((0, 0, 0))

        # When press quit, exit the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()