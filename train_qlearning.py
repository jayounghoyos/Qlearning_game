import numpy as np
from simple_game import SimpleGame

# Configuración del algoritmo Q-Learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.99  # Factor de descuento
epsilon = 1.0  # Tasa de exploración inicial
epsilon_decay = 0.995  # Decadencia de epsilon
min_epsilon = 0.01  # Epsilon mínimo

# Crear el entorno
env = SimpleGame()
state_size = env.state_size  # Tamaño del espacio de estados (ancho, alto)
action_size = len(env.actions)  # Número de acciones

# Ajustar `num_states` para incluir la tercera dimensión del estado
num_states = state_size[0] * state_size[1] * 60  # 60 es un límite arbitrario para obstacle_y

# Crear la Tabla Q
Q_table = np.zeros((num_states, action_size), dtype=np.float32)

# Función para mapear estado a índice único
def map_state_to_index(state):
    player_x, obstacle_x, obstacle_y = state
    return player_x + state_size[0] * (obstacle_x + 60 * obstacle_y)

# Entrenamiento del agente
episodes = 5000
for episode in range(episodes):
    state = map_state_to_index(env.reset())  # Mapear estado inicial a índice único
    done = False
    total_reward = 0

    while not done:
        # Elegir acción (exploración o explotación)
        if np.random.rand() < epsilon:
            action = np.random.choice(action_size)  # Exploración
        else:
            action = np.argmax(Q_table[state])  # Explotación

        # Tomar acción y observar resultados
        next_state, reward, done = env.step(action)
        next_state = map_state_to_index(next_state)  # Mapear estado siguiente a índice único

        # Actualizar la Tabla Q
        best_next_action = np.argmax(Q_table[next_state])
        Q_table[state, action] += alpha * (
            reward + gamma * Q_table[next_state, best_next_action] - Q_table[state, action]
        )

        state = next_state  # Actualizar estado actual
        total_reward += reward

    # Reducir epsilon (menos exploración con el tiempo)
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    print(f"Episodio: {episode + 1}, Recompensa Total: {total_reward}")

# Guardar la Tabla Q
np.save("q_table.npy", Q_table)
print("Entrenamiento completado. Tabla Q guardada.")
