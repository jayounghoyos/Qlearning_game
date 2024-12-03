import pygame
import numpy as np
import random

# Juego básico
class SimpleGame:
    def __init__(self):
        self.width = 400
        self.height = 600
        self.player_pos = [200, 500]
        self.obstacle_pos = [random.randint(0, self.width - 50), 0]
        self.obstacle_speed = 5
        self.actions = [0, 1]  # 0: Izquierda, 1: Derecha
        self.state_size = (self.width // 10, self.height // 10)  # Tamaño del espacio de estados

    def reset(self):
        self.player_pos = [200, 500]
        self.obstacle_pos = [random.randint(0, self.width - 50), 0]
        return self.get_state()

    def step(self, action):
        # Movimiento del jugador
        if action == 0 and self.player_pos[0] > 0:  # Izquierda
            self.player_pos[0] -= 10
        elif action == 1 and self.player_pos[0] < self.width - 50:  # Derecha
            self.player_pos[0] += 10

        # Movimiento del obstáculo
        self.obstacle_pos[1] += self.obstacle_speed
        if self.obstacle_pos[1] > self.height:  # Reiniciar obstáculo
            self.obstacle_pos = [random.randint(0, self.width - 50), 0]

        # Calcular recompensa
        reward = 1  # Recompensa por evitar el obstáculo
        done = False
        if self._check_collision():
            reward = -10  # Penalización por colisión
            done = True

        return self.get_state(), reward, done

    def get_state(self):
        # Discretizar el estado (posiciones del jugador y el obstáculo)
        player_x = max(0, min(self.player_pos[0] // 10, self.state_size[0] - 1))
        obstacle_x = max(0, min(self.obstacle_pos[0] // 10, self.state_size[0] - 1))
        obstacle_y = max(0, min(self.obstacle_pos[1] // 10, self.state_size[1] - 1))
        return (player_x, obstacle_x, obstacle_y)


    def render(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), (*self.player_pos, 50, 50))  # Jugador
        pygame.draw.rect(screen, (255, 0, 0), (*self.obstacle_pos, 50, 50))  # Obstáculo
        pygame.display.flip()

    def _check_collision(self):
        px, py = self.player_pos
        ox, oy = self.obstacle_pos
        return abs(px - ox) < 50 and abs(py - oy) < 50
