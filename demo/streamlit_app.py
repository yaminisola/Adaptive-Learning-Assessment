import streamlit as st
import time
import sys
import os

# Add the parent 'src' directory to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

# Initialize session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'intro'
    st.session_state.player_name = ''
    st.session_state.difficulty = 'medium'
    st.session_state.generator = PuzzleGenerator()
    st.session_state.tracker = PerformanceTracker()
    st.session_state.engine = AdaptiveEngine()
    st.session_state.current_puzzle = None
    st.session_state.puzzle_count = 0
    st.session_state.max_puzzles = 10
    st.session_state.start_time = None
    st.session_state.difficulty_history = []

# Page configuration
st.set_page_config(
    page_title="Math Adventures",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2em;
        font-weight: bold;
        padding: 0.75em;
        border-radius: 10px;
        border: none;
    }
    .puzzle-box {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        padding: 3em;
        border-radius: 20px;
        text-align: center;
        margin: 2em 0;
    }
    .puzzle-text {
        font-size: 3em;
        font-weight: bold;
        color: #333;
    }
    .stat-box {
        background: #f0f0f0;
        padding: 1em;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def start_game(name, diff):
    st.session_state.game_state = 'playing'
    st.session_state.player_name = name
    st.session_state.difficulty = diff
    st.session_state.puzzle_count = 0
    st.session_state.tracker = PerformanceTracker()
    st.session_state.difficulty_history = [diff]
    load_next_puzzle()

def load_next_puzzle():
    st.session_state.current_puzzle = st.session_state.generator.generate_puzzle(
        st.session_state.difficulty
    )
    st.session_state.start_time = time.time()

def submit_answer(user_answer):
    if user_answer is None:
        st.warning("Please enter an answer!")
        return
    
    end_time = time.time()
    time_taken = (end_time - st.session_state.start_time) * 1000
    
    puzzle = st.session_state.current_puzzle
    is_correct = user_answer == puzzle['answer']
    
    st.session_state.tracker.record_attempt(
        puzzle=puzzle,
        user_answer=user_answer,
        correct=is_correct,
        time_ms=time_taken,
        difficulty=st.session_state.difficulty
    )
    
    if is_correct:
        st.success(f"✓ Correct! The answer is {puzzle['answer']}")
    else:
        st.error(f"✗ Not quite! The answer was {puzzle['answer']}")
    
    st.session_state.puzzle_count += 1
    
    if st.session_state.puzzle_count >= st.session_state.max_puzzles:
        st.session_state.game_state = 'summary'
    else:
        # Adapt difficulty
        recent = st.session_state.tracker.get_recent_performance(3)
        new_diff = st.session_state.engine.adapt_difficulty(
            recent, 
            st.session_state.difficulty
        )
        if new_diff != st.session_state.difficulty:
            st.info(f"🔄 Difficulty adjusted: {st.session_state.difficulty.upper()} → {new_diff.upper()}")
        st.session_state.difficulty = new_diff
        st.session_state.difficulty_history.append(new_diff)
        
        time.sleep(2)
        load_next_puzzle()
        st.rerun()

def reset_game():
    st.session_state.game_state = 'intro'
    st.session_state.player_name = ''
    st.session_state.difficulty = 'medium'
    st.session_state.puzzle_count = 0
    st.session_state.difficulty_history = []
    st.rerun()

# ===== INTRO SCREEN =====
if st.session_state.game_state == 'intro':
    st.markdown("<h1 style='text-align: center; color: white;'>🧠 Math Adventures</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>AI-Powered Adaptive Learning</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        name = st.text_input("Your Name", placeholder="Enter your name")
        
        st.markdown("**Starting Difficulty**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Easy", key="easy_btn"):
                st.session_state.difficulty = 'easy'
        with col2:
            if st.button("Medium", key="medium_btn"):
                st.session_state.difficulty = 'medium'
        with col3:
            if st.button("Hard", key="hard_btn"):
                st.session_state.difficulty = 'hard'
        
        st.info(f"Selected: **{st.session_state.difficulty.upper()}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Adventure!", key="start_btn"):
            if name:
                start_game(name, st.session_state.difficulty)
                st.rerun()
            else:
                st.error("Please enter your name!")

# ===== PLAYING SCREEN =====
elif st.session_state.game_state == 'playing':
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<h3 style='color: white;'>Welcome, {st.session_state.player_name}!</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: white;'>Question {st.session_state.puzzle_count + 1}/{st.session_state.max_puzzles}</h2>", unsafe_allow_html=True)
    with col2:
        diff_color = {'easy': '#22c55e', 'medium': '#eab308', 'hard': '#ef4444'}
        st.markdown(f"<div style='background: {diff_color[st.session_state.difficulty]}; color: white; padding: 0.5em; border-radius: 10px; text-align: center; font-weight: bold;'>{st.session_state.difficulty.upper()}</div>", unsafe_allow_html=True)
    
    puzzle = st.session_state.current_puzzle
    if puzzle:
        st.markdown("<div class='puzzle-box'>", unsafe_allow_html=True)
        st.markdown(f"<div class='puzzle-text'>{puzzle['num1']} {puzzle['operation']} {puzzle['num2']} = ?</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        answer = st.number_input("Your Answer", value=None, step=1, key=f"answer_{st.session_state.puzzle_count}")
        
        if st.button("Submit Answer", key=f"submit_{st.session_state.puzzle_count}"):
            submit_answer(answer)
    
    # Stats
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        acc = st.session_state.tracker.calculate_accuracy()
        st.markdown(f"<div class='stat-box'><strong>🎯 Accuracy: {acc:.1f}%</strong></div>", unsafe_allow_html=True)
    with col2:
        avg_time = st.session_state.tracker.calculate_avg_time()
        st.markdown(f"<div class='stat-box'><strong>⏱️ Avg Time: {avg_time:.1f}s</strong></div>", unsafe_allow_html=True)

# ===== SUMMARY SCREEN =====
elif st.session_state.game_state == 'summary':
    st.markdown("<h1 style='text-align: center; color: white;'>🏆 Great Job!</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: white;'>{st.session_state.player_name}</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>Session Complete</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Summary stats
    total = len(st.session_state.tracker.history)
    correct = sum(1 for h in st.session_state.tracker.history if h['correct'])
    accuracy = st.session_state.tracker.calculate_accuracy()
    avg_time = st.session_state.tracker.calculate_avg_time()
    dist = st.session_state.tracker.get_difficulty_distribution()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col2:
        st.metric("Avg Time", f"{avg_time:.1f}s")
    with col3:
        st.metric("Correct", f"{correct}/{total}")
    with col4:
        st.metric("Final Level", st.session_state.difficulty.upper())
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Difficulty progression
    st.markdown("**📊 Difficulty Progression**")
    st.bar_chart({
        'Easy': dist['easy'],
        'Medium': dist['medium'],
        'Hard': dist['hard']
    })
    
    # Recommendation
    st.markdown("<br>", unsafe_allow_html=True)
    if accuracy >= 80 and st.session_state.difficulty == 'hard':
        st.success("🌟 Amazing! You mastered hard mode!")
    elif accuracy >= 80:
        st.info(f"📈 Ready to advance beyond {st.session_state.difficulty} level!")
    elif accuracy >= 60:
        st.info(f"💪 Keep practicing at {st.session_state.difficulty} level!")
    else:
        st.warning("🎯 Consider trying an easier level to build confidence!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Play Again"):
        reset_game()
