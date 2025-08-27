import pygame
import random
import math
from pygame import Vector2
from CONFIG import *

class Particle:
    def __init__(self, x, y, color):
        self.pos = Vector2(x, y)
        speed = random.uniform(*PARTICLE_SPEED)
        angle = random.uniform(0, 2 * 3.14159)
        self.velocity = Vector2(0, 0)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        self.velocity.x = vx
        self.velocity.y = vy
        self.color = color
        self.size = random.randint(*PARTICLE_SIZE)
        self.lifetime = random.randint(*PARTICLE_LIFETIME)
        self.alpha = 255

    def update(self):
        self.pos += self.velocity
        self.lifetime -= 1
        # Fade out particle as it gets closer to death
        self.alpha = int((self.lifetime / PARTICLE_LIFETIME[1]) * 255)
        return self.lifetime > 0

    def draw(self, screen):
        if self.alpha > 0:
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, self.alpha), (self.size, self.size), self.size)
            screen.blit(surf, (int(self.pos.x - self.size), int(self.pos.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color):
        for _ in range(PARTICLE_COUNT):
            self.particles.append(Particle(x, y, color))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
