# 🚀 Space Shooter Game

A fun and interactive **Space Shooter Game** built using **HTML5 Canvas, JavaScript, and CSS** — perfect for learning game development basics and practicing real-time rendering, animation, and user interaction.

---

## Deployment

You can try the live app here: [Space Shooter Game](https://space-shooter-game-hz7bnyry4iivrmuxxfzdh4.streamlit.app/)

## 🎮 About

This project is a **classic 2D space shooting game** where:

✔ A player controls a spaceship  
✔ The spaceship can move left/right  
✔ The player shoots enemies or objects  
✔ Score updates as you destroy targets  
✔ Game over on collision

It’s designed to demonstrate **core game mechanics** using browser technologies without any external libraries.

---

## 🧠 How It Works

### 🛸 Game Loop

The game uses a **main animation loop** that:

1. Draws the background and player  
2. Updates positions of enemies and bullets  
3. Checks for collisions  
4. Updates scores and game state  
5. Repaints the canvas every frame

This loop runs using `requestAnimationFrame()` to ensure smooth animation.

### 🎮 Player Controls

- **Left Arrow (←)**: Move spaceship left  
- **Right Arrow (→)**: Move spaceship right  
- **Space Bar**: Shoot bullets

### 🛠 Collision Detection

Each frame, the code checks if:

- A bullet hits an enemy  
- The player collides with an enemy

If a collision is detected, the score updates or the game ends accordingly.

---

## 🏗️ Project Structure

```

Space-Shooter-Game/
├── index.html         # Game canvas and UI
├── style.css          # Game styling and layout
├── script.js          # Game logic (player, enemies, bullets)
└── assets/            # Game images (spaceship, enemies, bullets, etc)

````

---

## 🚀 How to Play

### 📥 Clone the Repository

```bash
git clone https://github.com/Abhishek-Maurya-D/Space-Shooter-Game.git
cd Space-Shooter-Game
````

### 🕹️ Open in Browser

Open the `index.html` file in any modern browser (Chrome, Firefox, Edge).

---

## 📦 Gameplay

✔ Move your spaceship left or right
✔ Shoot enemies with the Space key
✔ Avoid enemy collisions
✔ Your score increases as you destroy enemies
✔ Game over when the player collides with enemy

The UI updates dynamically using JavaScript and Canvas drawing calls.

---

## ⚙️ Features

✨ Smooth animation with HTML5 Canvas
✨ Keyboard controls
✨ Score tracking
✨ Collision detection
✨ Game reset and restart logic

---

## 🛠 Tools & Technologies

* **HTML5** – Game canvas
* **CSS3** – Styles and layout
* **JavaScript** – Game logic & interaction
* **HTML5 Canvas** – Rendering graphics

---

## 🤝 Contributions

Contributions are welcome! You could:

✔ Add enemy waves
✔ Add sound effects
✔ Add levels/difficulty
✔ Add player lives
✔ Add mobile touch controls

📝 To contribute:

1. Fork this repo
2. Create a feature branch
3. Add your changes
4. Submit a Pull Request

---

## 📄 License

This project is meant for **educational and learning use**.

---

## 🙌 Thanks for Playing!

Thanks for checking out the Space Shooter Game!
Have fun coding and playing! 🚀🛸
