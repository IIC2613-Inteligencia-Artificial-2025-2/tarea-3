import pygame

class Obstacle:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)

def create_obstacles(obs_pos, obs_radius):
    obs = []
    for pos in obs_pos:
        obs.append(Obstacle(pos, obs_radius))
    return obs