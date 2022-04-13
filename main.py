import pygame
import math
pygame.init()


WIDTH, HEIGHT = 800, 800                            # WINDOW SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")     # TITLE

FONT = pygame.font.SysFont("cosolas", 16)

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)


class Planet:
    AU = 149.6e6 * 1000         # Distance from earth to sun
    G = 6.67428e-11             # Atraction between objects
    ZOOM = 100 / AU             # 200 / AU = 200 pixels per AU
    TIMESCALE = 3600*24         # 1300 = 1 day per second


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
        # 0 now equals center
        x = self.x * self.ZOOM + WIDTH / 2
        y = self.y * self.ZOOM + HEIGHT / 2


        # orbit drawn
        if len(self.orbit) > 2:
            orbit_points = []
            for point in self.orbit:
                orbit_x, orbit_y = point
                orbit_x = orbit_x * self.ZOOM + WIDTH / 2
                orbit_y = orbit_y * self.ZOOM + HEIGHT / 2
                orbit_points.append((orbit_x, orbit_y))

            pygame.draw.lines(window, self.color, False, orbit_points, 2)

        # draw planet
        pygame.draw.circle(window, self.color, (x, y), self.radius * self.ZOOM * 10**9)

        # drawn distance
        if not self.is_sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)} KM", 1, WHITE)
            window.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

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
            fx, fy = self.attraction(planet)
            total_force_x += fx
            total_force_y += fy
        
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

        # Draw planets and calculate position
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        # Draw fps
        fps = FONT.render(f"FPS: {round(delta_time.get_fps(), 2)}", 1, WHITE)
        WIN.blit(fps, (0, 0))
        # Draw time
        seconds = FONT.render(f"Seconds: {round(pygame.time.get_ticks() / 1000, 2)}", 1, WHITE)
        WIN.blit(seconds, (0, 1.5 * HEIGHT / 100))
        
        pygame.display.update()

    pygame.quit()

main()