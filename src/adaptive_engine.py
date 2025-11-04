class AdaptiveEngine:
    def __init__(self):
        # Thresholds for difficulty adjustment
        self.thresholds = {
            'advance_accuracy': 0.67,  # 2/3 correct
            'advance_performance': 0.75,
            'demote_accuracy': 0.34,    # 1/3 correct
            'demote_performance': 0.4,
            'high_performance': 0.8
        }
    
    def calculate_performance_score(self, recent_performance):
        """
        Calculate composite performance score
        Combines accuracy (70%) and speed (30%)
        
        Args:
            recent_performance (list): Recent attempt records
        
        Returns:
            tuple: (accuracy, speed_score, performance_score)
        """
        if not recent_performance:
            return 0.5, 0.5, 0.5
        
        # Calculate accuracy
        correct_count = sum(1 for p in recent_performance if p['correct'])
        accuracy = correct_count / len(recent_performance)
        
        # Calculate speed score (normalized, 15s baseline)
        avg_time = sum(p['time_ms'] for p in recent_performance) / len(recent_performance)
        speed_score = max(0, min(1, 1 - (avg_time / 15000)))
        
        # Composite performance score (accuracy weighted 70%, speed 30%)
        performance_score = (accuracy * 0.7) + (speed_score * 0.3)
        
        return accuracy, speed_score, performance_score
    
    def adapt_difficulty(self, recent_performance, current_difficulty):
        """
        Determine next difficulty level based on recent performance
        
        Algorithm:
        - Analyzes last 3 attempts
        - Computes accuracy and speed metrics
        - Uses rule-based logic for difficulty transitions
        
        Args:
            recent_performance (list): Recent attempt records
            current_difficulty (str): Current difficulty level
        
        Returns:
            str: New difficulty level ('easy', 'medium', or 'hard')
        """
        if len(recent_performance) < 2:
            return current_difficulty
        
        accuracy, speed_score, perf_score = self.calculate_performance_score(recent_performance)
        
        # Adaptive logic based on current difficulty
        if current_difficulty == 'easy':
            # Advance to medium if performing well
            if (perf_score > self.thresholds['advance_performance'] and 
                accuracy >= self.thresholds['advance_accuracy']):
                return 'medium'
                
        elif current_difficulty == 'medium':
            # Advance to hard if performing excellently
            if (perf_score > self.thresholds['high_performance'] and 
                accuracy >= self.thresholds['advance_accuracy']):
                return 'hard'
            # Demote to easy if struggling
            elif (perf_score < self.thresholds['demote_performance'] or 
                  accuracy < self.thresholds['demote_accuracy']):
                return 'easy'
                
        elif current_difficulty == 'hard':
            # Demote to medium if struggling
            if (perf_score < 0.5 or accuracy < self.thresholds['demote_accuracy']):
                return 'medium'
        
        return current_difficulty
