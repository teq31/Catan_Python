# 🎲 PyCatan - Settlers of Catan Clone

A fully functional implementation of the famous board game **Settlers of Catan**, built from scratch using **Python** and **Pygame**. 

This project simulates the core mechanics of the game, including board generation, resource management, building, trading (Bank & Player), ports, and all development cards.

## ✨ Features

* **Hexagonal Map Generation:** Randomly generates resources (Wood, Brick, Sheep, Wheat, Ore), number tokens, and **Ports**.
* **4-Player Support:** Play against 3 intelligent AI opponents.
* **Building System:**
    * Construction of **Roads**, **Settlements**, and **Cities**.
    * Validates placement rules (distance rule, connectivity).
* **Economic Engine:**
    * **Dice Rolling:** Distributes resources based on dice results.
    * **Robber Logic:** Blocks resource production and **steals** a random resource from a player on that tile.
    * **Ports:** Logic for 3:1 general ports and 2:1 specific resource ports.
* **Trading System:**
    * **Bank/Port Trade:** Dynamic exchange rates based on player's owned ports.
    * **Player-to-Player Trade:** Negotiate resource exchanges with AI players (AI evaluates offers based on needs).
* **Development Cards (Complete):**
    * **Knight:** Move the robber.
    * **Monopoly:** Steal all of one resource type from other players.
    * **Year of Plenty:** Take any 2 resources from the bank.
    * **Road Building:** Build 2 roads for free.
    * **Victory Point:** Automatically adds to the score.
* **Achievements:**
    * **Longest Road** (2 VP).
    * **Largest Army** (2 VP).
* **Save/Load System:** Persist game state using `pickle` (useful for demonstrating specific scenarios).
* **Win Condition:** The first player to reach **10 Victory Points** wins the game.

## 🛠️ Tech Stack

* **Language:** Python 3.12.8
* **Library:** Pygame (for rendering and input handling)

## 🎮 Controls

The game uses a combination of keyboard shortcuts and mouse interactions.

### General & Actions
| Key | Action |
| :--- | :--- |
| **`R`** | **Roll Dice** (Start of turn) |
| **`1`** | Build **Settlement** (Click vertex) |
| **`2`** | Build **Road** (Click edge) |
| **`3`** | Upgrade to **City** (Click settlement) |
| **`4`** | Buy **Development Card** |
| **`SPACE` / `ENTER`** | **End Turn** |
| **`ESC`** | Cancel current action / Back to View Mode |
| **`S`** | **Save** Game State |
| **`L`** | **Load** Game State |

### Trading & Cards
| Key | Action |
| :--- | :--- |
| **`T`** | Open **Bank/Port Trade** Menu |
| **`P`** | Open **Player Trade** Menu |
| **`K`** | Play **Knight Card** |
| **`M`** | Play **Monopoly Card** |
| **`Y`** | Play **Year of Plenty Card** |
| **`U`** | Play **Road Building Card** |

### Inside Player Trade Menu (P)
* **`W, B, S, G, O`**: Add resources to offer.
* **`TAB`**: Switch between "You Give" and "You Want".
* **`SPACE`**: Change trading partner (Cycle through players).
* **`ENTER`**: Propose Trade.

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

    *Tip: You can use the `S` key to save a game state when you reach an interesting point, and `L` to load it later for demonstration.*

## 🔮 Future Improvements

* Multiplayer support over LAN/Internet.
* Clickable UI buttons instead of keyboard shortcuts.
* Enhanced AI strategy (minimax or heuristic improvements).
* Animations for dice rolling and building.

---
*Developed by [Teodora Nechita]*