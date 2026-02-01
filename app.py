import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(page_title="Space Shooter Pro", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stCodeBlock { background-color: #000000 !important; border: 2px solid #00ff00 !important; font-family: 'Courier New'; }
    .score-text { color: #00ff00; font-size: 24px; font-weight: bold; }
    .lives-text { color: #ff3333; font-size: 20px; font-weight: bold; }
    .game-title { color: #00ffff; font-size: 32px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- Game Constants ---
WIDTH, HEIGHT = 25, 18
MAX_LIVES = 3

# --- Initialize Game State ---
if 'player_x' not in st.session_state:
    st.session_state.player_x = WIDTH // 2
if 'bullets' not in st.session_state:
    st.session_state.bullets = []
if 'enemies' not in st.session_state:
    st.session_state.enemies = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'lives' not in st.session_state:
    st.session_state.lives = MAX_LIVES
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'run_game' not in st.session_state:
    st.session_state.run_game = False
if 'level' not in st.session_state:
    st.session_state.level = 1

# --- Core Functions ---
def reset_game():
    st.session_state.player_x = WIDTH // 2
    st.session_state.bullets = []
    st.session_state.enemies = []
    st.session_state.score = 0
    st.session_state.lives = MAX_LIVES
    st.session_state.level = 1
    st.session_state.game_over = False
    st.session_state.run_game = True

def spawn_enemies():
    spawn_chance = 0.05 + st.session_state.level * 0.01
    if random.random() < spawn_chance:
        st.session_state.enemies.append([random.randint(0, WIDTH-1), 0, random.choice([1, 2])])  # type 1 or 2

def update_game_step():
    if st.session_state.game_over:
        return
    
    # Move bullets
    st.session_state.bullets = [[x, y-1] for [x, y] in st.session_state.bullets if y > 0]

    # Move enemies
    new_enemies = []
    for ex, ey, etype in st.session_state.enemies:
        ey += 1 + (etype-1)*0  # type 2 can be faster in future
        # Collision with player
        if ey >= HEIGHT - 1 and ex == st.session_state.player_x:
            st.session_state.lives -= 1
            if st.session_state.lives <= 0:
                st.session_state.game_over = True
        # Collision with bullets
        hit = False
        for bx, by in st.session_state.bullets:
            if bx == ex and by == ey:
                st.session_state.score += 10 * etype
                st.session_state.bullets.remove([bx, by])
                hit = True
                break
        if not hit and ey < HEIGHT:
            new_enemies.append([ex, ey, etype])
    st.session_state.enemies = new_enemies
    spawn_enemies()

# --- UI ---
st.markdown("<div class='game-title'>👾 SPACE SHOOTER PRO 👾</div>", unsafe_allow_html=True)
st.markdown(f"<div class='score-text'>SCORE: {st.session_state.score}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='lives-text'>LIVES: {'❤️'*st.session_state.lives}</div>", unsafe_allow_html=True)

board_placeholder = st.empty()

# Controls
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬅️ Left"):
        if st.session_state.player_x > 0: st.session_state.player_x -= 1
with col2:
    if st.button("🔥 SHOOT"):
        st.session_state.bullets.append([st.session_state.player_x, HEIGHT-2])
with col3:
    if st.button("➡️ Right"):
        if st.session_state.player_x < WIDTH-1: st.session_state.player_x += 1
with col4:
    if st.button("🔴 Reset"):
        reset_game()

# --- Game Loop ---
if st.session_state.run_game and not st.session_state.game_over:
    update_game_step()

    # Render
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    grid[HEIGHT-1][st.session_state.player_x] = "🚀"
    for bx, by in st.session_state.bullets:
        if 0 <= by < HEIGHT: grid[by][bx] = "¦"
    for ex, ey, etype in st.session_state.enemies:
        if 0 <= ey < HEIGHT: grid[ey][ex] = "👽" if etype==1 else "👾"
    
    board_placeholder.code("\n".join(["".join(row) for row in grid]), language="text")

    # Speed control
    time.sleep(0.1)
    st.rerun()

elif st.session_state.game_over:
    board_placeholder.error(f"💥 GAME OVER! FINAL SCORE: {st.session_state.score}")
    if st.button("PLAY AGAIN"):
        reset_game()
        st.rerun()
else:
    board_placeholder.info("Click '🔴 Reset' to start the game.")
