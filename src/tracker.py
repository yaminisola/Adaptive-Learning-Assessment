class PerformanceTracker:
    """Tracks user performance across problems"""
    
    def __init__(self):
        self.history = []
        self.difficulty_changes = 0
        self.last_difficulty = None
    
    def record_performance(self, puzzle, user_answer, correct_answer, is_correct, time_taken, difficulty):
        """
        Record performance for a single problem
        
        Args:
            puzzle (str): The problem string (e.g., "5 + 3")
            user_answer (float): User's answer
            correct_answer (float): Correct answer
            is_correct (bool): Whether answer was correct
            time_taken (float): Time in seconds
            difficulty (int): Difficulty level (1-3)
        """
        record = {
            'puzzle': puzzle,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'correct': is_correct,
            'time': time_taken,
            'difficulty': difficulty
        }
        
        self.history.append(record)
        
        # Track difficulty changes
        if self.last_difficulty is not None and self.last_difficulty != difficulty:
            self.difficulty_changes += 1
        self.last_difficulty = difficulty
    
    def get_history(self):
        """Get complete performance history"""
        return self.history
    
    def get_recent_performance(self, n=3):
        """
        Get recent performance metrics for ML model
        
        Args:
            n (int): Number of recent problems to analyze
        
        Returns:
            dict: Performance metrics
        """
        if not self.history:
            return {
                'accuracy': 0.0,
                'avg_time': 0.0,
                'correct_streak': 0,
                'incorrect_streak': 0,
                'recent_problems': 0,
                'trend': 0  # -1 declining, 0 stable, 1 improving
            }
        
        recent = self.history[-n:] if len(self.history) >= n else self.history
        
        # Calculate metrics
        correct_count = sum(1 for r in recent if r['correct'])
        total_count = len(recent)
        accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
        
        avg_time = sum(r['time'] for r in recent) / total_count if total_count > 0 else 0
        
        # Calculate streaks
        correct_streak = 0
        incorrect_streak = 0
        for record in reversed(recent):
            if record['correct']:
                correct_streak += 1
                if incorrect_streak > 0:
                    break
            else:
                incorrect_streak += 1
                if correct_streak > 0:
                    break
        
        # Calculate trend (comparing first half vs second half of recent)
        trend = 0
        if len(recent) >= 4:
            mid = len(recent) // 2
            first_half_acc = sum(1 for r in recent[:mid] if r['correct']) / mid
            second_half_acc = sum(1 for r in recent[mid:] if r['correct']) / (len(recent) - mid)
            
            if second_half_acc > first_half_acc + 0.2:
                trend = 1  # Improving
            elif second_half_acc < first_half_acc - 0.2:
                trend = -1  # Declining
        
        return {
            'accuracy': accuracy,
            'avg_time': avg_time,
            'correct_streak': correct_streak,
            'incorrect_streak': incorrect_streak,
            'recent_problems': total_count,
            'trend': trend
        }
    
    def get_summary(self):
        """
        Get comprehensive session summary
        
        Returns:
            dict: Complete performance summary
        """
        if not self.history:
            return {}
        
        total_problems = len(self.history)
        correct = sum(1 for r in self.history if r['correct'])
        incorrect = total_problems - correct
        accuracy = (correct / total_problems) * 100
        
        total_time = sum(r['time'] for r in self.history)
        avg_time = total_time / total_problems
        
        # Difficulty distribution
        difficulty_dist = {1: 0, 2: 0, 3: 0}
        for record in self.history:
            difficulty_dist[record['difficulty']] += 1
        
        # Performance by difficulty
        perf_by_diff = {1: {'correct': 0, 'total': 0}, 
                        2: {'correct': 0, 'total': 0}, 
                        3: {'correct': 0, 'total': 0}}
        
        for record in self.history:
            diff = record['difficulty']
            perf_by_diff[diff]['total'] += 1
            if record['correct']:
                perf_by_diff[diff]['correct'] += 1
        
        # Final difficulty and recommendation
        final_difficulty = self.history[-1]['difficulty']
        
        # Recommend next difficulty based on final performance
        recent_perf = self.get_recent_performance(3)
        if recent_perf['accuracy'] >= 80 and final_difficulty < 3:
            recommended = final_difficulty + 1
        elif recent_perf['accuracy'] < 50 and final_difficulty > 1:
            recommended = final_difficulty - 1
        else:
            recommended = final_difficulty
        
        return {
            'total_problems': total_problems,
            'correct': correct,
            'incorrect': incorrect,
            'accuracy': accuracy,
            'avg_time': avg_time,
            'difficulty_distribution': difficulty_dist,
            'difficulty_changes': self.difficulty_changes,
            'final_difficulty': final_difficulty,
            'recommended_difficulty': recommended,
            'performance_by_difficulty': perf_by_diff,
            'model_info': {
                'type': 'Logistic Regression',
                'predictions_made': total_problems - 1,
                'last_confidence': recent_perf['accuracy'] / 100
            }
        }
    
    def export_data(self):
        """
        Export data in format suitable for ML training
        
        Returns:
            list: List of feature dictionaries
        """
        export = []
        for i, record in enumerate(self.history):
            # Get context from previous problems
            if i > 0:
                prev_correct = self.history[i-1]['correct']
                prev_time = self.history[i-1]['time']
            else:
                prev_correct = None
                prev_time = 0
            
            export.append({
                'problem_num': i + 1,
                'difficulty': record['difficulty'],
                'correct': record['correct'],
                'time': record['time'],
                'prev_correct': prev_correct,
                'prev_time': prev_time,
            })
        
        return export


# Testing
if __name__ == "__main__":
    tracker = PerformanceTracker()
    
    # Simulate some performance data
    test_data = [
        ("5 + 3", 8, 8, True, 3.2, 1),
        ("7 - 2", 5, 5, True, 2.8, 1),
        ("9 + 1", 10, 10, True, 2.1, 1),
        ("15 + 8", 23, 23, True, 4.5, 2),
        ("12 * 3", 36, 36, True, 5.2, 2),
        ("20 - 7", 12, 13, False, 8.3, 2),
        ("25 + 15", 40, 40, True, 6.1, 2),
    ]
    
    for puzzle, user_ans, correct_ans, is_correct, time, diff in test_data:
        tracker.record_performance(puzzle, user_ans, correct_ans, is_correct, time, diff)
    
    print("Testing Performance Tracker\n")
    print("=" * 50)
    print("\nRecent Performance:")
    print(tracker.get_recent_performance())
    print("\nSummary:")
    for key, value in tracker.get_summary().items():
        print(f"{key}: {value}")
