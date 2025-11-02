This is a vey bad python project,i try to make a doom-like fps game with python but idk y its so laggy
u can play with it anyway.I dont want to make a exe for it bc its rlly to bad to play.
and idk will i update it again.
Heres the real README:
Game Overview
This is a first-person shooter game similar to the classic Doom, implemented using Python and Pygame. The game uses raycasting technology to achieve 3D effects and includes enemy AI, weapon systems, and multiple levels.

<img width="807" height="811" alt="屏幕截图 2025-11-02 141050" src="https://github.com/user-attachments/assets/81912a5c-f834-4b7b-83d3-66c6ea762157" />

Game Objectives
Primary Goal: Eliminate all enemies in each level

Secondary Goal: Maintain high health and achieve high scores

Game Mechanics
1. Health System
Player starts with 100 health points

Health decreases when attacked by enemies

Game ends when health reaches 0

2. Ammunition System
Player starts with 50 rounds of ammunition

Each shot consumes 1 round

Cannot fire when out of ammo

3. Scoring System
Eliminate an enemy: +100 points

Current score displayed in top-right corner

4. Enemy Types
Standard Enemy (Red): Normal movement speed and attack power

Fast Enemy (Light Red): Faster movement speed

Enemies will patrol, chase the player, and attack when close

Game Interface
1. 3D Main View
3D environment rendered using raycasting technology

Walls have different textures

Enemies appear as sprites

2. HUD (Heads-Up Display)
Top Left: Health text and health bar

Top Right: Ammo count and current score

Screen Center: Crosshair

Bottom Center: Weapon animation

3. Game State Indicators
Playing: Normal game view

Game Over: Shows "GAME OVER" and final score

Level Complete: Shows "YOU WIN!" and final score

Level System
The game includes 2 levels:

Level 1
Map Size: 10×10

Enemies: 2 standard enemies

Relatively simple, good for learning game mechanics

Level 2
Map Size: 12×12

Enemies: 2 standard enemies + 2 fast enemies

More complex map with varied enemies

Strategy Tips
1. Movement Strategies
Use strafing (Q/E keys) to dodge enemy attacks

Retreat in narrow areas, advance in open spaces

Use walls for cover

2. Combat Strategies
Maintain distance to avoid being surrounded

Prioritize eliminating fast enemies

Use corners for ambushes

3. Resource Management
Conserve ammo, ensure each shot has high accuracy

Monitor health to avoid unnecessary damage


Troubleshooting
If you encounter issues:

Ensure all files are in the same folder

Check if required libraries are installed
If experiencing performance issues:

Try reducing screen resolution (modify SCREEN_WIDTH and SCREEN_HEIGHT in settings.py)

Close other running applications

ame Tips
Use Field of View: Enemies are only rendered in your field of view - use this for tactical movement

Audio Cues: Pay attention to enemy movement sounds (if audio is implemented)

Learn the Maps: Each level has a fixed layout - learn it for better route planning

Keep Moving: Staying still makes you an easy target for enemy attacks

Expansion Possibilities
This game framework can be further expanded:

Add more weapon types

Implement health packs and ammo pickups

Add background music and sound effects

Create more complex maps and enemy AI

Add multiplayer game mode

Enjoy the game! If you encounter any issues, please refer to the code comments or check error messages for debugging.
