# AI

## I. A* Algorithm

### 1. The Problem with Cubes
  We are given M cubes that are put in N stacks. We have the initial configuration and have to apply the A* algorithm to reach the Goal configuration. We can move only the cubes that are placed on top. Links: [Problem requirement](https://drive.google.com/drive/folders/1-b8lHmrSZTDLMr80QjPv_2Iyhb6NL519), [Github](https://github.com/AndraRaco/AI/blob/master/Algoritmul%20A%20star/Problema%20blocurilor.py)
  
### 2. 8-puzzle
  8-Puzzle is a popular puzzle that consists of N tiles where N can be 8, 15, 24 and so on. In our example N = 8. The puzzle is divided into sqrt(N+1) rows and sqrt(N+1) columns. The puzzle can be solved by moving the tiles one by one in the single empty space and thus achieving the Goal configuration. Links: [Problem requirement](https://drive.google.com/drive/folders/1-b8lHmrSZTDLMr80QjPv_2Iyhb6NL519), [Github](https://github.com/AndraRaco/AI/blob/master/Algoritmul%20A%20star/8-puzzle.py)

### 3. The Missionaries and Cannibals Problem
  In the missionaries and cannibals problem, N missionaries and N cannibals must cross a river using a boat which can carry at most M people, under the constraint that, for both banks, if there are missionaries present on the bank, they cannot be outnumbered by cannibals (if they were, the cannibals would eat the missionaries). The boat cannot cross the river by itself with no people on board. Links: [Problem requirement](https://drive.google.com/drive/folders/1-b8lHmrSZTDLMr80QjPv_2Iyhb6NL519), [Github](https://github.com/AndraRaco/AI/blob/master/Algoritmul%20A%20star/Problema%20canibalilor%20si%20misionarilor.py)

### 4. Search problem 
  The students are placed in benches in the classroom. One of the students wants to send a written message to other student who is placed somewhere else in the class. Some benches are empty and some children are angry with each other. The message can be passed to the next column only through last two rows. Links: [Problem requirement(first problem)](https://drive.google.com/drive/folders/1-b8lHmrSZTDLMr80QjPv_2Iyhb6NL519), [Github](https://github.com/AndraRaco/AI/blob/master/Algoritmul%20A%20star/Problema%20de%20cautare%20(mesaj).py)
  
## II. Minimax Algorithm and Alpha-Beta pruning

### 1. Tic-Tac-Toe
  This is an implementation of a Tic-Tac-Toe solver using the Minimax Algorithm and also Alpha-Beta pruning to help the AI to make decisions. Tic-tac-toe is a paper-and-pencil game for two players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row is the winner. Links: [Problem requirement](https://drive.google.com/drive/folders/1_yPjMZjoC5ccjDDAHNqd42w9J_lUnEdP), [Github](https://github.com/AndraRaco/AI/blob/master/Minimax%20Algorithm%20and%20Alpha-Beta%20pruning/Tic-Tac-Toe.py).

### 2. Connect 4
  Connect Four is a two-player board game in which the players first choose a symbol (X or 0) and then take turns dropping one disc from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs. Links: [Problem requirement](https://drive.google.com/drive/folders/1_yPjMZjoC5ccjDDAHNqd42w9J_lUnEdP), [Github](https://github.com/AndraRaco/AI/blob/master/Minimax%20Algorithm%20and%20Alpha-Beta%20pruning/Connect%204.py).
  
### 3. Reversi/ Othello
  Reversi is a strategy board game for two players, played on an 8×8 uncheckered board. There are sixty-four identical game pieces called disks (often spelled "discs"), which are light on one side and dark on the other. Players take turns placing disks on the board with their assigned color facing up. During a play, any disks of the opponent's color that are in a straight line and bounded by the disk just placed and another disk of the current player's color are turned over to the current player's color. The object of the game is to have the majority of disks turned to display your color when the last playable empty square is filled. Links: [Problem requirement](https://drive.google.com/drive/folders/1_yPjMZjoC5ccjDDAHNqd42w9J_lUnEdP), [Github](https://github.com/AndraRaco/AI/blob/master/Minimax%20Algorithm%20and%20Alpha-Beta%20pruning/Reversi.py).
  
