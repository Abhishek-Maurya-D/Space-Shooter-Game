import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- Page Config & Styling ---
st.set_page_config(page_title="Pro Space Shooter", layout="centered")

# JavaScript to capture key presses and click hidden buttons
# This mimics the _kbhit() and _getch() functionality from your C++ code
st.components.v1.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            doc.querySelector('button[kind="secondary"]:nth-child(1)').click();
        } else if (e.key === 'ArrowRight') {
            doc.querySelector('button[kind="secondary"]:nth-child(2)').click();
        } else if (e.key === ' ') {
            doc.querySelector('button[kind="secondary"]:nth-child(3)').click();
        } else if (e.key === 'Enter') {
            doc.querySelector('button[kind="primary"]').click();
        }
    });
    </script>
    """,
    height=0,
)

st.markdown("""
    <style>
    .reportview-container { background: #000; }
    .stCodeBlock { background-color: #000 !important; border: 1px solid #1f1f1f !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Constants ---
WIDTH = 30
HEIGHT = 20

# --- Game State ---
if 'player_x' not in st.session_state:
    st.session_state.update({
        'player_x': WIDTH // 2,
        'bullets': [],
        'enemies': [],
        'score': 0,
        'game_over': False,
        'init': False
    })

# --- Helper Functions ---
def shoot():
    st.session_state.bullets.append([st.session_state.player_x, HEIGHT - 2])

def move_left():
    if st.session_state.player_x > 1: st.session_state.player_x -= 1

def move_right():
    if st.session_state.player_x < WIDTH - 2: st.session_state.player_x += 1

def reset():
    st.session_state.update({
        'player_x': WIDTH // 2, 'bullets': [], 'enemies': [],
        'score': 0, 'game_over': False, 'init': True
    })

# --- Auto-Update Engine ---
# This refreshes the game state every 100ms (similar to Sleep(30))
if st.session_state.init and not st.session_state.game_over:
    st_autorefresh(interval=100, key="gameloop")

# --- Game Logic Update ---
if st.session_state.init and not st.session_state.game_over:
    # Move Bullets
    st.session_state.bullets = [[x, y-1] for x, y in st.session_state.bullets if y > 0]
    
    # Move Enemies
    new_enemies = []
    for ex, ey in st.session_state.enemies:
        ey += 1
        # Collision Check
        if ex == st.session_state.player_x and ey >= HEIGHT - 1:
            st.session_state.game_over = True
        
        hit = False
        for b in st.session_state.bullets:
            if b[0] == ex and (b[1] == ey or b[1] == ey - 1):
                st.session_state.score += 10
                st.session_state.bullets.remove(b)
                hit = True
                break
        
        if not hit and ey < HEIGHT:
            new_enemies.append([ex, ey])
    st.session_state.enemies = new_enemies

    # Spawn Enemies
    if random.random() < 0.1:
        st.session_state.enemies.append([random.randint(1, WIDTH-2), 0])

# --- UI Rendering ---
st.title("🚀 Keyboard Space Shooter")
st.subheader(f"Score: {st.session_state.score}")

# Render the Board
grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
# Draw Player
grid[HEIGHT-1][st.session_state.player_x] = "A"
# Draw Bullets
for bx, by in st.session_state.bullets:
    grid[by][bx] = "|"
# Draw Enemies
for ex, ey in st.session_state.enemies:
    grid[ey][ex] = "V"

board_text = "\n".join(["".join(row) for row in grid])
st.code(board_text, language="text")

# --- Hidden Controls (Used by JavaScript) ---
# We keep these visible for manual play, but JS clicks them automatically
col1, col2, col3 = st.columns(3)
with col1: st.button("Left", on_click=move_left)
with col2: st.button("Right", on_click=move_right)
with col3: st.button("Space (Fire)", on_click=shoot)

if st.session_state.game_over:
    st.error("GAME OVER!")
    st.button("Enter (Restart)", on_click=reset, type="primary")
elif not st.session_state.init:
    st.button("Enter (Start Game)", on_click=reset, type="primary")

st.info("🎮 Use Arrow Keys to Move | Space to Shoot | Enter to Start/Restart")
