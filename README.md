# ⚫⚪ Othello Classic AI ⚪⚫

This repository contains the source code for a classic Othello (Reversi) game built in Python. The game features a full graphical user interface (GUI) using **`tkinter`**, audio support via **`pygame`**, and a challenging single-player mode against an AI powered by the **Minimax algorithm** with Alpha-Beta pruning.

> 💡 **Quick Start:** To play, clone the repository, install the dependencies from `requirements.txt`, and run `python Othello.py`. For a full list of features and setup instructions, see the sections below.

---

## 📌 Project Overview

This repository contains a fully-featured Othello (Reversi) game built with Python. The project combines a robust game engine with a polished, interactive GUI and a challenging AI opponent. Below is a summary of its core components, followed by a detailed guide to its features.

### High-Level Features

- **Game Engine:**
  - Full implementation of Othello rules, including piece flipping, valid move calculation, and end-game conditions.
  - A modular structure that separates the game logic from the user interface.
- **Graphical User Interface (GUI):**
  - Built entirely with Python's standard **`tkinter`** library.
  - A multi-screen interface including a splash screen, main menu, options, and game board.
  - Interactive elements created with `tkinter.Canvas` for a custom look and feel.
- **AI Opponent:**
  - An AI player based on the **Minimax algorithm** to find the optimal move.
  - **Alpha-Beta pruning** is implemented to significantly improve the AI's decision-making speed.
  - Three adjustable difficulty levels (Easy, Normal, Hard) that control the algorithm's search depth.
- **Gameplay Experience & Customization:**
  - **Visual Personalization:** Tailor the game's appearance with a variety of selectable board themes and unique piece designs.
  - **Audio Settings:** Manage the game's audio with separate controls for background music and in-game sound effects.
  - **Strategic Flexibility:** A handy "Undo" feature is available, allowing players to reverse their most recent move.
  - **Player Guidance:** An integrated "How to Play" guide, complete with visual aids, explains the rules and game mechanics for new players.

### Main Menu Functionality

The main menu is the central hub of the application, providing access to all game modes and settings:

- **One Player (Player vs. AI):**
  - In this mode, you challenge the AI opponent. Before the game begins, a setup screen appears, allowing you to:
    - Choose your piece color (Black or White).
    - Select the AI's difficulty level from the three available options.

- **Two Players (Player vs. Player):**
  - This mode allows you to play a classic Othello match against a friend locally on the same computer. The game proceeds with each player taking turns.

- **Options:**
  - This section lets you fully personalize your gaming experience. The available settings include:
    - **Board Theme:** You can choose from several visual themes for the game board, including **Green** (Default), **Red**, **Blue**, and a special **"Batman vs. Superman"** theme.
    - **Piece Style:** The appearance of the game pieces can be changed by selecting from several unique style sets, including **Default** (classic black and white discs), **Gems** (ruby and sapphire stones), and the special **BVS** theme (Batman and Superman logos).
    - **Audio Controls:** You can independently toggle the **Background Music** and **Sound Effects** (like the piece placement sound) on or off.

- **How to Play:**
  - A comprehensive section designed to help new players, which includes two parts:
    - **Instructions:** General guidance on how to navigate the menus and use the game's features.
    - **Game Rules:** A detailed explanation of the rules of Othello, accompanied by **images** to clearly illustrate key concepts like how to capture opponent pieces.

- **Exit:**
  - To prevent accidentally closing the game, this option displays a confirmation dialog asking if you are sure you want to exit the application.

---

## 🗂️ Repository Structure
```
Othello_Classic_AI_Project/
├── Photo/                  # Contains all images for themes, pieces, and UI elements
├── Othello.py              # Main application script with game logic and GUI
├── requirements.txt        # Python dependencies
└── README.md               # This document
```

> You can add a `screenshots/` folder to store images of the game for the README.

---

## 🛠️ Requirements & Setup

### 1) Install Python packages
Make sure you have Python 3.x installed. The external libraries required for this project (`pygame`, `Pillow`) are listed in the `requirements.txt` file. You can install them with a single command:
```bash
pip install -r requirements.txt
```
> 💡 **Note:** Other libraries used, such as `tkinter`, `os`, and `math`, are part of Python's Standard Library and do not require separate installation.

### 2) Run the game
Execute the main Python script from your terminal to launch the game:
```bash
python Othello.py
```

---

## 📊 Outputs (Screenshots)
It is highly recommended to add screenshots of your application to showcase its features visually.

*(Example of how to add images in Markdown)*
```markdown
![Main Menu](link_to_your_screenshot.jpg)
```

| Main Menu | Options Screen |
| :---: | :---: |
| *(Your Screenshot Here)* | *(Your Screenshot Here)* |

---

## 🧩 Tech Stack
- **Python 3.x**
- **tkinter:** For the graphical user interface.
- **Pillow (PIL Fork):** Used for loading, resizing, and processing images for the GUI.
- **pygame:** For loading and playing background music and sound effects.

---

## ❓ FAQ

**Q: Can I run this project without installing any libraries?** A: No, you must install `pygame` and `Pillow` first. You can do this easily by running `pip install -r requirements.txt`.

**Q: How do I change the theme or piece style?** A: From the main menu, go to the "Options" screen. There you can select your preferred board theme and piece style. The changes will be applied to your next game.

**Q: Is the AI beatable?** A: Yes, especially on the "Easy" and "Normal" difficulty settings. The "Hard" setting provides a significant challenge as the AI searches deeper for the best possible move.
