# WumpusMind

WumpusMind is a modern, interactive web-based implementation of the classic Artificial Intelligence problem: **The Wumpus World**. 

Designed to visually demonstrate how intelligent agents reason under uncertainty, WumpusMind features a sleek UI, smooth animations, and a powerful Hybrid Agent capable of propositional logic, Bayesian probability, and heuristic search.

## ✨ Features

- **Dynamic Environments**: Customize grid sizes (from classic 4x4 up to 10x10) and difficulty levels (Easy, Medium, Hard) to control hazard density.
- **Manual Play Mode**: Navigate the grid yourself using keyboard controls (WASD or Arrows) or an on-screen D-pad. The AI will still act as your "advisor," computing risks in the background.
- **Autoplay / AI Mode**: Watch autonomous agents attempt to conquer the maze.
  - **Hybrid Agent**: A state-of-the-art agent that combines a Propositional Knowledge Base, First-Order Logic reasoning, a Bayesian Probability Engine, and A* Pathfinding.
  - **Pure A* Baseline**: A simpler algorithmic baseline that blindly explores the maze using only pathfinding heuristics without reasoning about hazards.
- **Risk Heatmap**: Toggle a visual probability heatmap to see exactly how the Hybrid Agent calculates the risk of hidden Pits or the Wumpus on unvisited tiles.
- **Live Reasoning Log**: See the AI's "thoughts" in real-time. The reasoning log outputs logic deductions (e.g., "No breeze at (0,1), so (0,2) has no Pit") and probability thresholds.
- **Modern UI & Animations**: Built with CSS custom properties and GSAP for responsive, smooth gameplay.

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/WumpusMind.git
   cd WumpusMind
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The primary dependency is `Flask`. Standard Python libraries are used for the AI logic.)*

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Play:**
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## 🎮 How to Play

**The Goal**: Find the **Gold** (✨) and grab it without dying to win the game!

**Percepts & Hints**:
- 🌬️ **Breeze**: You feel a breeze. There is a deadly **Pit** in one of the adjacent (up, down, left, right) cells.
- 🤢 **Stench**: You smell something awful. The deadly **Wumpus** is in an adjacent cell.
- ✨ **Glitter**: You found the gold! (The agent will automatically grab it).

**Hazards**:
- **Pits (🕳️)**: Stepping into a pit is instant death.
- **The Wumpus (👹)**: Stepping onto the Wumpus cell is instant death.

## 🧠 Under the Hood: The Hybrid Agent

The **Hybrid Agent** is the core AI of WumpusMind, combining multiple layers of reasoning:
1. **Knowledge Base (KB)**: Stores safe cells, visited cells, and known hazard locations.
2. **Propositional Logic**: Applies forward chaining. For example, if a cell has no breeze, it mathematically proves that all adjacent cells are free of pits.
3. **Bayesian Probability Engine**: When no guaranteed safe cells are left, the agent calculates the marginal probability of a hazard existing in unknown cells based on the distribution of known breezes and stenches. It then picks the cell with the lowest risk.
4. **A* Pathfinding**: Once a target cell is chosen (either proven safe or calculated as lowest risk), the agent uses A* search to navigate safely through the known maze to reach it.

## 🛠️ Technology Stack
- **Backend**: Python 3, Flask (API & Routing)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Animations**: [GSAP (GreenSock)](https://greensock.com/gsap/)
