from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine
import time

def main():
    print("=" * 50)
    print("🎓 MATH ADVENTURES - Adaptive Learning System")
    print("=" * 50)
    
    # Initialize components
    generator = PuzzleGenerator()
    tracker = PerformanceTracker()
    engine = AdaptiveEngine()
    
    # Get user info
    player_name = input("\nEnter your name: ").strip()
    print(f"\nWelcome, {player_name}!")
    
    # Choose initial difficulty
    print("\nChoose starting difficulty:")
    print("1. Easy (ages 5-7)")
    print("2. Medium (ages 7-9)")
    print("3. Hard (ages 9-10)")
    
    choice = input("Enter choice (1-3): ").strip()
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    current_difficulty = difficulty_map.get(choice, 'medium')
    
    print(f"\nStarting at {current_difficulty.upper()} level!")
    print("\nAnswer 10 questions. Let's begin!\n")
    
    # Main game loop
    max_puzzles = 10
    for i in range(max_puzzles):
        print(f"\n--- Question {i+1}/{max_puzzles} ---")
        print(f"Current Level: {current_difficulty.upper()}")
        
        # Generate puzzle
        puzzle = generator.generate_puzzle(current_difficulty)
        print(f"\n{puzzle['num1']} {puzzle['operation']} {puzzle['num2']} = ?")
        
        # Get answer and measure time
        start_time = time.time()
        try:
            user_answer = int(input("Your answer: "))
        except ValueError:
            user_answer = -999
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # ms
        is_correct = user_answer == puzzle['answer']
        
        # Feedback
        if is_correct:
            print("✓ Correct!")
        else:
            print(f"✗ Incorrect. The answer was {puzzle['answer']}")
        
        # Track performance
        tracker.record_attempt(
            puzzle=puzzle,
            user_answer=user_answer,
            correct=is_correct,
            time_ms=response_time,
            difficulty=current_difficulty
        )
        
        # Adapt difficulty
        if i >= 2:  # Need at least 3 attempts
            new_difficulty = engine.adapt_difficulty(
                tracker.get_recent_performance(3),
                current_difficulty
            )
            if new_difficulty != current_difficulty:
                print(f"\n🔄 Difficulty adjusted: {current_difficulty.upper()} → {new_difficulty.upper()}")
            current_difficulty = new_difficulty
    
    # Display summary
    print("\n" + "=" * 50)
    print("📊 SESSION SUMMARY")
    print("=" * 50)
    tracker.display_summary(player_name)

if __name__ == "__main__":
    main()
