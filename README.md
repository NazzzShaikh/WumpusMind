# WumpusMind

WumpusMind is a web-based implementation of the classic Wumpus World AI problem. It features an interactive UI and multiple AI agents that demonstrate reasoning and pathfinding.

## Features

- **Customizable Grid**: Play on grids ranging from 4x4 to 10x10.
- **Difficulty Levels**: Choose between Easy, Medium, and Hard (affects Wumpus and Pit density).
- **Manual Mode**: Play the game yourself using WASD, Arrow keys, or the on-screen D-pad. The AI reasoning log will still provide advice.
- **Autoplay Mode (AI)**: Watch the AI play the game autonomously. Includes two algorithms:
  - **Hybrid Agent**: Uses a Propositional Knowledge Base, First-Order Logic, a Bayesian Probability Engine, and A* Search to make informed decisions.
  - **Pure A* Baseline**: A simple baseline that uses only A* pathfinding to explore unvisited cells blindly.
- **Probability Heatmap**: A toggleable visual heatmap that shows the Hybrid Agent's calculated risk percentages for unvisited cells.
- **Reasoning Log**: A live feed showing the AI's deductions, probability calculations, and chosen actions.

## Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML, CSS, Vanilla JavaScript, GSAP (for animations)
- **AI Modules**: Pure Python implementations of BFS, A*, Propositional Logic, and Bayesian inference (`agent_hybrid.py`, `fol_engine.py`, `probability_engine.py`, `search.py`).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/WumpusMind.git
   cd WumpusMind
   ```

2. Create a virtual environment (Optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000/`.
