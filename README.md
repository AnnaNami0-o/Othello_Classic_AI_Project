🎮 Othello Classic AI 🎮
This repository contains the source code for a classic Othello (Reversi) game built in Python. The game features a full graphical user interface (GUI) using tkinter, audio support via pygame, and a challenging single-player mode against an AI powered by the Minimax algorithm with Alpha-Beta pruning.

💡 Quick Start: To play, clone the repository, install the dependencies listed in requirements.txt, and run the main Python script. For a full list of features and setup instructions, see the sections below.

📌 Project Overview
The workflow and features implemented in Othello.py include:

Game Engine:

Full implementation of Othello rules, including piece flipping, valid move calculation, and end-game conditions.

A modular structure that separates the game logic from the user interface.

Graphical User Interface (GUI):

Built entirely with Python's standard tkinter library.

A multi-screen interface including a splash screen, main menu, options, and game board.

Interactive elements created with tkinter.Canvas for a custom look and feel.

AI Opponent:

An AI player based on the Minimax algorithm to find the optimal move.

Alpha-Beta pruning is implemented to significantly improve the AI's decision-making speed by cutting off branches of the game tree that don't need to be searched.

Three adjustable difficulty levels (Easy, Normal, Hard) that control the search depth of the algorithm.

Customization & Features:

Multiple Themes: Players can choose from different board colors and piece styles, including a special "Batman vs. Superman" theme.

Sound Control: Background music and sound effects can be toggled on or off in the options menu.

Undo Move: A feature to take back the last move.

In-Game Help: A "How to Play" section with images explaining the rules of Othello.

🗂️ Repository Structure
Othello_Classic_AI_Project/
├── Photo/                  # Contains all images for themes, pieces, and UI elements
├── Othello.py              # Main application script with game logic and GUI
├── requirements.txt        # Python dependencies
└── README.md               # This document
🛠️ Requirements & Setup
1) Install Python packages
Make sure you have Python 3.x installed. Then, install the required dependencies from the requirements.txt file.

Bash

pip install -r requirements.txt
2) Run the game
Execute the main Python script from your terminal to launch the game.

Bash

python Othello.py
📊 Outputs (Screenshots)
It is highly recommended to add screenshots of your application to showcase its features visually. You can add images of:

The main menu

The options screen showing the different themes

The game board during a match with a custom theme enabled

(Example of how to add images in Markdown)
![Main Menu](link_to_your_screenshot.jpg)

🧩 Tech Stack
Python 3.x

tkinter: For the graphical user interface.

Pillow (PIL Fork): Used for loading, resizing, and processing images for the GUI.

pygame: For loading and playing background music and sound effects.

❓ FAQ
Q: Can I run this project without installing any libraries?
A: No, you must install pygame and Pillow first. You can do this easily by running pip install -r requirements.txt.

Q: How do I change the theme or piece style?
A: From the main menu, go to the "Options" screen. There you can select your preferred board theme and piece style. The changes will be applied to your next game.

Q: Is the AI beatable?
A: Yes, especially on the "Easy" and "Normal" difficulty settings. The "Hard" setting provides a significant challenge as the AI searches deeper for the best possible move.
