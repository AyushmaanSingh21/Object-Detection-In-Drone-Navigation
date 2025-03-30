import numpy as np

# Define problem space (Grid-based path)
GRID_SIZE = (10, 10)  # 10x10 Grid for path planning
START = (0, 0)  # Start position of the drone
TARGET = (9, 9)  # Target position
OBSTACLES = [(4, 5), (5, 5), (6, 5)]  # Obstacles

# Harmony Search Parameters
HMS = 5  # Harmony memory size (number of solutions)
HMCR = 0.9  # Harmony memory consideration rate
PAR = 0.3  # Pitch adjustment rate
ITERATIONS = 100

# Initialize Harmony Memory (Random Paths)
harmony_memory = [np.random.randint(0, GRID_SIZE[0], size=(10, 2)) for _ in range(HMS)]


def fitness(path):
    """Fitness function to evaluate path quality."""
    score = 0
    for step in path:
        if tuple(step) in OBSTACLES:
            score += 50  # Penalize paths hitting obstacles
        else:
            score += np.linalg.norm(np.array(step) - np.array(TARGET))  # Distance to target
    return score


def harmony_search():
    """Perform Harmony Search Optimization."""
    global harmony_memory

    for iteration in range(ITERATIONS):
        new_path = []

        for step in range(10):  # Path of 10 steps
            if np.random.rand() < HMCR:
                # Select from Harmony Memory
                selected_harmony = harmony_memory[np.random.randint(0, HMS)]
                new_step = selected_harmony[step]
            else:
                # Generate a new step randomly
                new_step = np.random.randint(0, GRID_SIZE[0], size=(2,))

            # Pitch Adjustment
            if np.random.rand() < PAR:
                new_step += np.random.choice([-1, 1], size=(2,))  # Small adjustment

            # Ensure the step stays within bounds
            new_step = np.clip(new_step, 0, GRID_SIZE[0] - 1)

            new_path.append(new_step)

        new_path = np.array(new_path)
        new_fitness = fitness(new_path)

        # Replace worst harmony if the new path is better
        worst_index = np.argmax([fitness(h) for h in harmony_memory])
        if new_fitness < fitness(harmony_memory[worst_index]):
            harmony_memory[worst_index] = new_path

    return harmony_memory[np.argmin([fitness(h) for h in harmony_memory])]


# Run Harmony Search Algorithm
optimal_path = harmony_search()
print("Optimized Path:", optimal_path)
