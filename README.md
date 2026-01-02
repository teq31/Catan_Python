# 🎲 PyCatan - Settlers of Catan Clone

A fully functional implementation of the famous board game **Settlers of Catan**, built from scratch using **Python** and **Pygame**. 

This project simulates the core mechanics of the game, including board generation, resource management, building, trading, ports, and all development cards.

## ✨ Features

* **Hexagonal Map Generation:** Randomly generates resources (Wood, Brick, Sheep, Wheat, Ore), number tokens, and **Ports**.
* **Building System:**
    * Construction of **Roads**, **Settlements**, and **Cities**.
    * Validates placement rules (distance rule, connectivity).
* **Economic Engine:**
    * **Dice Rolling:** Distributes resources based on dice results.
    * **Robber Logic:** Blocks resource production on specific tiles when a 7 is rolled.
    * **Ports:** Logic for 3:1 general ports and 2:1 specific resource ports.
* **Trading System:**
    * **Bank/Port Trade:** Dynamic exchange rates based on player's owned ports.
* **Development Cards (Complete):**
    * **Knight:** Move the robber.
    * **Monopoly:** Steal all of one resource type from other players.
    * **Year of Plenty:** Take any 2 resources from the bank.
    * **Road Building:** Build 2 roads for free.
    * **Victory Point:** Automatically adds to the score.
* **Achievements:**
    * **Longest Road** (2 VP).
    * **Largest Army** (2 VP).
* **AI Opponent:** A functional AI that builds, trades, and competes for victory.
* **Save/Load System:** Persist game state using `pickle`.
* **Win Condition:** The first player to reach **10 Victory Points** wins the game.

## 🛠️ Tech Stack

* **Language:** Python 3.12.8
* **Library:** Pygame (for rendering and input handling)

## 🎮 Controls

The game uses a combination of keyboard shortcuts and mouse interactions.

| Key | Action |
| :--- | :--- |
| **`R`** | **Roll Dice** (Start of turn) |
| **`1`** | Build **Settlement** (Click vertex) |
| **`2`** | Build **Road** (Click edge) |
| **`3`** | Upgrade to **City** (Click settlement) |
| **`4`** | Buy **Development Card** |
| **`T`** | Open **Trade Menu** (Follow on-screen steps) |
| **`K`** | Play **Knight Card** (Move Robber) |
| **`M`** | Play **Monopoly Card** (Steal resource) |
| **`Y`** | Play **Year of Plenty Card** (Get 2 resources) |
| **`U`** | Play **Road Building Card** (Build 2 roads) |
| **`S`** | **Save** Game |
| **`L`** | **Load** Game |
| **`SPACE` / `ENTER`** | **End Turn** |
| **`ESC`** | Cancel current action / Back to View Mode |

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Catan-Python-Game.git](https://github.com/YOUR_USERNAME/Catan-Python-Game.git)
    cd Catan-Python-Game
    ```

2.  **Install dependencies:**
    Make sure you have Python installed, then install pygame:
    ```bash
    pip install pygame
    ```

3.  **Run the game:**
    * For the standard game:
        ```bash
        python main.py
        ```
    * For the 4-player God Mode demo:
        ```bash
        python demo.py
        ```

## 🔮 Future Improvements

* Multiplayer support over LAN/Internet.
* Clickable UI buttons instead of keyboard shortcuts.
* Enhanced AI strategy (minimax or heuristic improvements).
* Animations for dice rolling and building.

---
*Developed by [Teodora Nechita]*
