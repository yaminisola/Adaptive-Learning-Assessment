"""
Math Adventures - Streamlit Web Interface
AI-Powered Adaptive Learning System
FULLY CORRECTED VERSION - All errors fixed
"""

import streamlit as st
import time
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

# Page config
st.set_page_config(
    page_title="Math Adventures",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-top: 0;
    }
    .problem-display {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin: 20px 0;
    }
    .feedback-correct {
        padding: 20px;
        background-color: #d4edda;
        border: 2px solid #28a745;
        border-radius: 10px;
        color: #155724;
        font-size: 1.2em;
        text-align: center;
    }
    .feedback-incorrect {
        padding: 20px;
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        border-radius: 10px;
        color: #721c24;
        font-size: 1.2em;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.game_state = 'welcome'
        st.session_state.user_name = ''
        st.session_state.current_difficulty = 1
        st.session_state.puzzle_count = 0
        st.session_state.max_puzzles = 10
        st.session_state.generator = PuzzleGenerator()
        st.session_state.tracker = PerformanceTracker()
        st.session_state.engine = AdaptiveEngine()
        st.session_state.current_puzzle = None
        st.session_state.start_time = None
        st.session_state.feedback = None
        st.session_state.show_next_button = False

def start_game(name, difficulty):
    """Start a new game session"""
    st.session_state.user_name = name
    st.session_state.current_difficulty = difficulty
    st.session_state.game_state = 'playing'
    st.session_state.puzzle_count = 0
    st.session_state.tracker = PerformanceTracker()
    st.session_state.engine = AdaptiveEngine()
    generate_new_puzzle()

def generate_new_puzzle():
    """Generate a new puzzle"""
    st.session_state.current_puzzle = st.session_state.generator.generate_puzzle(
        st.session_state.current_difficulty
    )
    st.session_state.start_time = time.time()
    st.session_state.feedback = None
    st.session_state.show_next_button = False

def submit_answer(answer):
    """Process submitted answer - CORRECTED VERSION"""
    if st.session_state.current_puzzle is None:
        return
    
    # Calculate time taken
    time_taken = time.time() - st.session_state.start_time
    
    # Get correct answer
    correct_answer = st.session_state.current_puzzle['answer']
    
    # Check correctness
    is_correct = abs(float(answer) - correct_answer) < 0.01
    
    # Create puzzle string
    puzzle_str = f"{st.session_state.current_puzzle['num1']} {st.session_state.current_puzzle['operation']} {st.session_state.current_puzzle['num2']}"
    
    # Record performance - using correct method
    st.session_state.tracker.record_performance(
        puzzle=puzzle_str,
        user_answer=float(answer),
        correct_answer=correct_answer,
        is_correct=is_correct,
        time_taken=time_taken,
        difficulty=st.session_state.current_difficulty
    )
    
    # Store feedback
    st.session_state.feedback = {
        'is_correct': is_correct,
        'time': time_taken,
        'correct_answer': correct_answer,
        'user_answer': float(answer)
    }
    
    # Increment puzzle count
    st.session_state.puzzle_count += 1
    
    # Show next button
    st.session_state.show_next_button = True
    
    # Check if session is complete
    if st.session_state.puzzle_count >= st.session_state.max_puzzles:
        st.session_state.game_state = 'summary'
        return
    
    # Get recent performance metrics
    recent_perf = st.session_state.tracker.get_recent_performance(n=3)
    
    # Store old difficulty
    old_difficulty = st.session_state.current_difficulty
    
    # CORRECTED: Predict next difficulty using the correct method
    st.session_state.current_difficulty = st.session_state.engine.predict_next_difficulty(
        recent_perf,
        st.session_state.current_difficulty
    )
    
    # Store difficulty change info
    if old_difficulty != st.session_state.current_difficulty:
        st.session_state.feedback['difficulty_changed'] = True
        st.session_state.feedback['old_difficulty'] = old_difficulty
        st.session_state.feedback['new_difficulty'] = st.session_state.current_difficulty
        
        if st.session_state.current_difficulty > old_difficulty:
            st.session_state.feedback['change_reason'] = 'Excellent performance! Level UP! 🚀'
        else:
            st.session_state.feedback['change_reason'] = 'Let\'s practice at this level 💪'

def next_puzzle():
    """Move to next puzzle"""
    generate_new_puzzle()

def reset_game():
    """Reset the game"""
    st.session_state.game_state = 'welcome'
    st.session_state.puzzle_count = 0
    st.session_state.current_puzzle = None
    st.session_state.feedback = None
    st.session_state.show_next_button = False

# Initialize
init_session_state()

# Main UI
if st.session_state.game_state == 'welcome':
    # Welcome Screen
    st.markdown('<p class="main-header">🧮 Math Adventures</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Adaptive Learning System</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📚 How it works:")
        st.info("""
        - You'll solve 10 math problems
        - The system uses **Machine Learning** to adapt difficulty
        - Performance is tracked in real-time
        - Get personalized recommendations
        """)
        
        name = st.text_input("👤 Enter your name:", key="name_input")
        
        st.markdown("### 🎯 Choose starting difficulty:")
        difficulty = st.radio(
            "",
            [1, 2, 3],
            format_func=lambda x: ["🟢 Easy (Addition & Subtraction, 1-10)", 
                                    "🟡 Medium (All operations, 10-20)", 
                                    "🔴 Hard (All operations, 20-50)"][x-1],
            key="difficulty_input"
        )
        
        st.markdown("")
        if st.button("🚀 Start Adventure!", type="primary", use_container_width=True):
            if name.strip():
                start_game(name, difficulty)
                st.rerun()
            else:
                st.error("Please enter your name!")

elif st.session_state.game_state == 'playing':
    # Playing Screen
    st.markdown(f'<p class="main-header">Hello, {st.session_state.user_name}! 👋</p>', unsafe_allow_html=True)
    
    # Progress bar
    progress = st.session_state.puzzle_count / st.session_state.max_puzzles
    st.progress(progress)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Problem", f"{st.session_state.puzzle_count + 1}/{st.session_state.max_puzzles}")
    with col2:
        difficulty_labels = {1: "🟢 Easy", 2: "🟡 Medium", 3: "🔴 Hard"}
        st.metric("Difficulty", difficulty_labels[st.session_state.current_difficulty])
    
    st.markdown("---")
    
    # Display current puzzle
    if st.session_state.current_puzzle:
        puzzle_text = f"{st.session_state.current_puzzle['num1']} {st.session_state.current_puzzle['operation']} {st.session_state.current_puzzle['num2']} = ?"
        st.markdown(f'<div class="problem-display">{puzzle_text}</div>', unsafe_allow_html=True)
    
    # Answer input and submit
    if not st.session_state.show_next_button:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            answer = st.number_input("Your answer:", key="answer_input", label_visibility="collapsed")
            if st.button("Submit Answer", type="primary", use_container_width=True):
                if answer is not None:
                    submit_answer(answer)
                    st.rerun()
    
    # Display feedback
    if st.session_state.feedback:
        st.markdown("---")
        if st.session_state.feedback['is_correct']:
            st.markdown(f"""
            <div class="feedback-correct">
                ✅ Correct! 🎉<br>
                <small>Time: {st.session_state.feedback['time']:.1f} seconds</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-incorrect">
                ❌ Wrong! Correct answer was: {st.session_state.feedback['correct_answer']}<br>
                <small>Your answer: {st.session_state.feedback['user_answer']}</small><br>
                <small>Time: {st.session_state.feedback['time']:.1f} seconds</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Show difficulty change
        if st.session_state.feedback.get('difficulty_changed'):
            if st.session_state.feedback['new_difficulty'] > st.session_state.feedback['old_difficulty']:
                st.success(f"🚀 {st.session_state.feedback.get('change_reason', 'Level UP!')}")
            else:
                st.info(f"💪 {st.session_state.feedback.get('change_reason', 'Adjusting difficulty')}")
        
        # Next button
        if st.session_state.show_next_button:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Next Problem ➡️", type="primary", use_container_width=True):
                    if st.session_state.puzzle_count >= st.session_state.max_puzzles:
                        st.session_state.game_state = 'summary'
                    else:
                        next_puzzle()
                    st.rerun()
    
    # Current stats
    st.markdown("---")
    st.markdown("### 📊 Current Session Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Correct", st.session_state.tracker.get_correct_count())
    with col2:
        st.metric("❌ Incorrect", st.session_state.tracker.get_incorrect_count())
    with col3:
        acc = st.session_state.tracker.calculate_accuracy()
        st.metric("🎯 Accuracy", f"{acc:.0f}%")

elif st.session_state.game_state == 'summary':
    # Summary Screen
    st.markdown('<p class="main-header">🏆 Session Complete!</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Great job, {st.session_state.user_name}!</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    summary = st.session_state.tracker.get_summary()
    
    # Overall stats
    st.markdown("## 📊 Overall Performance")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Accuracy", f"{summary['accuracy']:.1f}%")
    with col2:
        st.metric("⏱️ Avg Time", f"{summary['avg_time']:.1f}s")
    with col3:
        st.metric("🔄 Level Changes", summary['difficulty_changes'])
    
    st.markdown("---")
    
    # Performance by difficulty
    st.markdown("## 📈 Performance by Difficulty")
    difficulty_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
    
    for level in [1, 2, 3]:
        perf = summary['performance_by_difficulty'][level]
        if perf['total'] > 0:
            acc = (perf['correct'] / perf['total']) * 100
            st.markdown(f"**{difficulty_labels[level]}:** {perf['correct']}/{perf['total']} correct ({acc:.0f}%)")
    
    st.markdown("---")
    
    # Detailed log
    st.markdown("## 📝 Detailed Problem Log")
    history = st.session_state.tracker.get_history()
    
    for i, record in enumerate(history, 1):
        status = "✅" if record['correct'] else "❌"
        diff_label = difficulty_labels[record['difficulty']]
        
        with st.expander(f"Problem {i}: {record['puzzle']} = {record['correct_answer']} {status}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Your answer:** {record['user_answer']}")
            with col2:
                st.write(f"**Time:** {record['time']:.1f}s")
            with col3:
                st.write(f"**Difficulty:** {diff_label}")
    
    st.markdown("---")
    
    # ML Model insights
    st.markdown("## 🤖 ML Model Insights")
    st.info(f"""
    **Model Type:** {summary['model_info']['type']}  
    **Predictions Made:** {summary['model_info']['predictions_made']}  
    **Final Confidence:** {summary['model_info']['last_confidence']:.2%}
    """)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("## 💡 Recommendations")
    if summary['accuracy'] >= 80:
        st.success("""
        🌟 **Excellent work!** You're ready for more challenges!
        
        📚 **Suggested next steps:**
        - Try starting at a higher difficulty
        - Focus on improving your speed
        """)
    elif summary['accuracy'] >= 60:
        st.info("""
        👍 **Good progress!** Keep practicing!
        
        📚 **Suggested next steps:**
        - Review problems you got wrong
        - Practice more at current difficulty
        """)
    else:
        st.warning("""
        💪 **Keep going!** Practice makes perfect!
        
        📚 **Suggested next steps:**
        - Start with easier problems
        - Take your time to understand each concept
        """)
    
    st.markdown(f"**Recommended starting difficulty for next session:** {difficulty_labels[summary['recommended_difficulty']]}")
    
    st.markdown("---")
    
    # Play again button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            reset_game()
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.info("""
    This is an **AI-Powered Adaptive Learning System** that uses:
    - **Machine Learning** (Logistic Regression)
    - Real-time performance tracking
    - Dynamic difficulty adjustment
    
    The system adapts to your performance to keep you in the optimal learning zone!
    """)
    
    st.markdown("---")
    st.markdown("### 📚 Features")
    st.markdown("""
    - ✨ ML-powered adaptation
    - 📊 Real-time tracking
    - 🎯 3 difficulty levels
    - 📈 Detailed analytics
    - 🤖 Transparent AI
    """)
    
    if st.session_state.game_state == 'playing':
        st.markdown("---")
        st.markdown("### 🎮 Quick Stats")
        st.write(f"Problems: {st.session_state.puzzle_count}/{st.session_state.max_puzzles}")
        st.write(f"Accuracy: {st.session_state.tracker.calculate_accuracy():.0f}%")
        if st.session_state.tracker.get_total_problems() > 0:
            st.write(f"Avg Time: {st.session_state.tracker.calculate_avg_time():.1f}s")
