import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(page_title="Streamlit Space Invaders", layout="centered")

# --- Custom Styling (Arcade Look) ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stCodeBlock { background-color: #000000 !important; border: 2px solid #00ff00 !important; }
    .score-text { font-family: 'Courier New'; color: #00ff00; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- Game Constants ---
WIDTH = 25
HEIGHT = 18

# --- Initialize Game State ---
if 'player_x' not in st.session_state:
    st.session_state.player_x = WIDTH // 2
if 'bullets' not in st.session_state:
    st.session_state.bullets = []
if 'enemies' not in st.session_state:
    st.session_state.enemies = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'run_game' not in st.session_state:
    st.session_state.run_game = False

# --- Core Logic Functions ---
def reset_game():
    st.session_state.player_x = WIDTH // 2
    st.session_state.bullets = []
    st.session_state.enemies = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.run_game = True

def update_game_step():
    if st.session_state.game_over:
        return

    # 1. Move Bullets
    st.session_state.bullets = [[x, y-1] for [x, y] in st.session_state.bullets if y > 0]

    # 2. Move Enemies
    new_enemies = []
    for ex, ey in st.session_state.enemies:
        ey += 1
        # Collision with Player
        if ex == st.session_state.player_x and ey >= HEIGHT - 1:
            st.session_state.game_over = True
        
        # Collision with Bullets
        hit = False
        for bx, by in st.session_state.bullets:
            if bx == ex and (by == ey or by == ey - 1):
                st.session_state.score += 10
                st.session_state.bullets.remove([bx, by])
                hit = True
                break
        
        if not hit and ey < HEIGHT:
            new_enemies.append([ex, ey])
    st.session_state.enemies = new_enemies

    # 3. Spawn Enemies
    if random.random() < 0.15:
        st.session_state.enemies.append([random.randint(0, WIDTH-1), 0])

# --- UI Layout ---
st.title("👾 Space Shooter Pro")
st.markdown(f"<div class='score-text'>SCORE: {st.session_state.score}</div>", unsafe_allow_html=True)

# Game Display Area
board_placeholder = st.empty()

# Controls Area
ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns(4)

with ctrl_col1:
    if st.button("⬅️ Left"):
        if st.session_state.player_x > 0: st.session_state.player_x -= 1
with ctrl_col2:
    if st.button("🔥 SHOOT"):
        st.session_state.bullets.append([st.session_state.player_x, HEIGHT - 2])
with ctrl_col3:
    if st.button("➡️ Right"):
        if st.session_state.player_x < WIDTH - 1: st.session_state.player_x += 1
with ctrl_col4:
    if st.button("🔴 Stop/Reset"):
        reset_game()

# --- The Game Loop ---
# This loop simulates the C++ while(isGameRunning)
if st.session_state.run_game and not st.session_state.game_over:
    # Update logic
    update_game_step()
    
    # Render frame
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    grid[HEIGHT-1][st.session_state.player_x] = "▲" # Player
    for bx, by in st.session_state.bullets:
        if 0 <= by < HEIGHT: grid[by][bx] = "¦" # Bullets
    for ex, ey in st.session_state.enemies:
        if 0 <= ey < HEIGHT: grid[ey][ex] = "👽" # Enemies (using emoji for better look)

    board_string = "\n".join(["".join(row) for row in grid])
    board_placeholder.code(board_string, language="text")

    # Control Game Speed
    time.sleep(0.1) 
    st.rerun()

elif st.session_state.game_over:
    board_placeholder.error(f"💥 GAME OVER! FINAL SCORE: {st.session_state.score}")
    if st.button("PLAY AGAIN"):
        reset_game()
        st.rerun()
else:
    board_placeholder.info("Click '🔴 Stop/Reset' to initialize the engine.")
