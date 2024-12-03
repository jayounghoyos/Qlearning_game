import numpy as np
from simple_game import SimpleGame

# Cargar la Tabla Q entrenada
Q_table = np.load('q_table.npy')

# Crear el entorno
env = SimpleGame()
state_size = env.state_size  # Tamaño del espacio de estados (ancho, alto)
action_size = len(env.actions)

# Función para mapear estado a índice único
def map_state_to_index(state):
    player_x, obstacle_x, obstacle_y = state
    return player_x + state_size[0] * (obstacle_x + 60 * obstacle_y)

# Probar el modelo entrenado
state = map_state_to_index(env.reset())  # Mapear estado inicial a índice único
done = False
total_reward = 0

while not done:
    action = np.argmax(Q_table[state])  # Tomar la mejor acción conocida
    next_state, reward, done = env.step(action)
    next_state = map_state_to_index(next_state)  # Mapear estado siguiente a índice único
    state = next_state
    total_reward += reward

    env.render()  # Renderizar el juego

print(f"Recompensa total en la evaluación: {total_reward}")
