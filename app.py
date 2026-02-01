import streamlit as st
import random
import time

# --- Configuration & Styling ---
st.set_page_config(page_title="Space Shooter", layout="centered")
st.markdown("""
    <style>
    .game-container {
        background-color: #000;
        color: #0f0;
        font-family: 'Courier New', Courier, monospace;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #333;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Game Logic Classes ---

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SpaceShooter:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        
        # Initialize session state for game variables
        if 'player_x' not in st.session_state:
            st.session_state.player_x = width // 2
        if 'bullets' not in st.session_state:
            st.session_state.bullets = []
        if 'enemies' not in st.session_state:
            st.session_state.enemies = []
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'game_over' not in st.session_state:
            st.session_state.game_over = False

    def move_player(self, direction):
        if direction == "left" and st.session_state.player_x > 0:
            st.session_state.player_x -= 1
        elif direction == "right" and st.session_state.player_x < self.width - 1:
            st.session_state.player_x += 1

    def shoot(self):
        st.session_state.bullets.append([st.session_state.player_x, self.height - 2])

    def update(self):
        if st.session_state.game_over:
            return

        # Move bullets
        new_bullets = []
        for b in st.session_state.bullets:
            b[1] -= 1
            if b[1] >= 0:
                new_bullets.append(b)
        st.session_state.bullets = new_bullets

        # Move enemies and handle collisions
        new_enemies = []
        if random.random() < 0.2:  # Enemy generation frequency
            st.session_state.enemies.append([random.randint(0, self.width - 1), 0])

        for e in st.session_state.enemies:
            e[1] += 1
            
            # Check collision with player
            if e[0] == st.session_state.player_x and e[1] == self.height - 1:
                st.session_state.game_over = True

            # Check collision with bullets
            hit = False
            for b in st.session_state.bullets:
                if b[0] == e[0] and b[1] == e[1]:
                    st.session_state.score += 10
                    st.session_state.bullets.remove(b)
                    hit = True
                    break
            
            if not hit and e[1] < self.height:
                new_enemies.append(e)
        
        st.session_state.enemies = new_enemies

    def render(self):
        # Create a grid
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw player
        grid[self.height - 1][st.session_state.player_x] = "▲"
        
        # Draw bullets
        for b in st.session_state.bullets:
            grid[b[1]][b[0]] = "¦"
            
        # Draw enemies
        for e in st.session_state.enemies:
            grid[e[1]][e[0]] = "▼"

        # Convert grid to string
        game_board = ""
        for row in grid:
            game_board += "|" + "".join(row) + "|\n"
        
        return game_board

# --- Streamlit UI ---

st.title("🚀 C++ Style Space Shooter")
game = SpaceShooter()

if st.session_state.game_over:
    st.error(f"GAME OVER! Final Score: {st.session_state.score}")
    if st.button("Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    # Instructions & Score
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Use the buttons below to move and shoot!")
    with col2:
        st.metric("Score", st.session_state.score)

    # Render Game Board
    game.update()
    board_output = game.render()
    st.code(board_output, language="text")

    # Controls
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⬅️ Left"):
            game.move_player("left")
            st.rerun()
    with c2:
        if st.button("🔥 Shoot"):
            game.shoot()
            st.rerun()
    with c3:
        if st.button("➡️ Right"):
            game.move_player("right")
            st.rerun()
    with c4:
        if st.button("🔄 Wait"):
            st.rerun()

    st.info("Note: In Streamlit, each action requires a button click to 'tick' the game forward.")
