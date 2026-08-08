# WumpusMind

**Hybrid Intelligent Wumpus World Agent**
*A college semester AI project demonstrating logical deduction, probabilistic inference, and pathfinding in an animated web application.*

## Live Demo
[Link to Render Deployment Placeholder]

## Project Overview
This project rebuilds the classic Wumpus World AI assignment from scratch as a polished, interactive web application. It features a custom-built Hybrid Agent that combines multiple AI paradigms to survive and thrive in a randomized hazard grid.

The UI is built with HTML/Vanilla JS and styled with CSS Grid, featuring GSAP for smooth animations and transitions.

## AI Concepts Demonstrated
WumpusMind allows you to step through the agent's thought process in real-time or run different algorithms against each other.

### 1. Knowledge Base (Propositional Logic)
The agent maintains a Knowledge Base (KB) and uses forward chaining rules (e.g., `NOT Breeze(x,y) ⟹ adjacent cells NOT Pit`) to deduce safe cells with 100% certainty based on the absence of percepts.

### 2. First-Order Logic (Resolution)
When stenches are detected, the agent uses First-Order Logic style intersection across multiple stench locations to pinpoint the exact coordinates of the Wumpus.

### 3. Bayesian Probability (Risk Inference)
When logical deduction fails to find a guaranteed safe move, the agent switches to probabilistic reasoning. It calculates a Joint Risk score for every unvisited cell based on the prior probabilities of hazards and the number of adjacent percepts (Breeze/Stench). This is visualized as an in-game Heatmap overlay.

### 4. Search & Pathfinding (A* and BFS)
- **A***: The Hybrid Agent uses the A* algorithm with a Manhattan distance heuristic to find the shortest safe path to its chosen target cell.
- **BFS**: Provided as a baseline, a pure Breadth-First Search agent blindly explores the grid, demonstrating the high mortality rate of uninformed search in Wumpus World.

## Local Setup

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open your browser to `http://localhost:5000`

## Deployment
This application is fully configured for deployment on Render as a Python Web Service. 
The provided `render.yaml` and `requirements.txt` instruct Render to use `gunicorn` as the WSGI HTTP server to serve the Flask application.
