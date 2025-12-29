# 🎲 PyCatan - Settlers of Catan Clone

A fully functional implementation of the famous board game **Settlers of Catan**, built from scratch using **Python** and **Pygame**. 

This project simulates the core mechanics of the game, including board generation, resource management, building, trading, and development cards.


## ✨ Features

* **Hexagonal Map Generation:** Randomly generates resources (Wood, Brick, Sheep, Wheat, Ore) and number tokens.
* **Building System:**
    * Construction of **Roads**, **Settlements**, and **Cities**.
    * Validates placement rules (distance rule, connectivity).
* **Economic Engine:**
    * **Dice Rolling:** Distributes resources based on dice results.
    * **Robber Logic:** Blocks resource production on specific tiles when a 7 is rolled.
* **Trading System:**
    * **Bank Trade:** Exchange 4 of the same resource for 1 of any resource.
* **Development Cards:**
    * Buy cards using resources.
    * Play **Knight Cards** to move the robber.
    * **Victory Point Cards** automatically add to the score.
* **Win Condition:** The first player to reach **10 Victory Points** wins the game.

## 🛠️ Tech Stack

* **Language:** Python 3.x
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
    ```bash
    python main.py
    ```

## 🔮 Future Improvements

* Implementation of the initial setup phase (placing the first 2 settlements/roads for free).
* "Longest Road" and "Largest Army" bonus points.
* Multiplayer support over LAN/Internet.
* Clickable UI buttons instead of keyboard shortcuts.

---
*Developed by [Teodora Nechita]*
