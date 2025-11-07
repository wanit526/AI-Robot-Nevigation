# 🤖 AI Robot Navigation (A* Algorithm)

This project simulates an **Automated Guided Vehicle (AGV)** in a warehouse environment, tasked with finding the most efficient path to its destination.

It demonstrates the practical application of the **A\* (A-Star) Algorithm**, a core Artificial Intelligence (AI) concept used in robotics, navigation systems, and video game development.

## 🚀 Features

* **Smart Pathfinding:**
    Utilizes the A\* algorithm to compute and find the "shortest path" from the start node (green) to the end node (red).
* **Obstacle Avoidance:**
    The AI can analyze the map and dynamically generate a path that successfully navigates around obstacles (walls/shelving, black).
* **Dynamic Simulation:**
    Visualizes the robot's (blue) movement along the calculated path (yellow) in real-time using Pygame.
* **Modular Map:**
    The environment map (the `MAP_GRID` variable) can be easily modified to test the AI's ability to find new paths in different layouts.

## 🔧 Technology Used

* **Python 3** (e.g., 3.12)
* **Pygame:** For creating the GUI, drawing the grid, and simulating movement.
* **python-pathfinding:** A third-party library providing the A\* (A-Star) algorithm.

## 📸 Screenshot
![Program Screenshot](<img width="598" height="446" alt="image" src="https://github.com/user-attachments/assets/cd966278-00b0-415e-aa1e-9a8b4adc0301" />)

## 🎬 How to Run

1.  Clone this repository or download the `.py` file.
2.  Install the required libraries (in your Terminal):
    ```bash
    python -m pip install pygame
    python -m pip install pathfinding
    ```
3.  Run the script:
    ```bash
    python robot_navigation.py
    ```
