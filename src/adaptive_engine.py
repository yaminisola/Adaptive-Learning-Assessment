import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class AdaptiveEngine:
    """
    ML-based adaptive difficulty engine using Logistic Regression
    
    The model learns to predict whether to:
    - Increase difficulty (class 2)
    - Keep same difficulty (class 1) 
    - Decrease difficulty (class 0)
    
    Based on features:
    - Current accuracy
    - Average response time
    - Correct/incorrect streaks
    - Performance trend
    - Current difficulty level
    """
    
    def __init__(self):
        # Initialize ML model
        self.model = LogisticRegression(
            multi_class='multinomial',
            solver='lbfgs',
            max_iter=1000,
            random_state=42
        )
        self.scaler = StandardScaler()
        
        # Pretrain with synthetic data (simulates experienced students)
        self._pretrain_model()
        
        # Track predictions
        self.prediction_count = 0
        self.last_confidence = 0.0
    
    def _pretrain_model(self):
        """
        Pretrain model with synthetic data representing various student behaviors
        This allows the model to work immediately without needing real training data
        """
        np.random.seed(42)
        
        # Generate synthetic training data
        # Features: [accuracy, avg_time, correct_streak, incorrect_streak, trend, current_difficulty]
        # Labels: 0 (decrease), 1 (stay), 2 (increase)
        
        training_data = []
        training_labels = []
        
        # Scenario 1: High performers (should increase difficulty)
        for _ in range(100):
            accuracy = np.random.uniform(80, 100)
            avg_time = np.random.uniform(2, 5)
            correct_streak = np.random.randint(2, 4)
            incorrect_streak = 0
            trend = 1
            current_diff = np.random.randint(1, 3)
            
            training_data.append([accuracy, avg_time, correct_streak, incorrect_streak, trend, current_diff])
            training_labels.append(2)  # Increase difficulty
        
        # Scenario 2: Struggling students (should decrease difficulty)
        for _ in range(100):
            accuracy = np.random.uniform(0, 40)
            avg_time = np.random.uniform(8, 15)
            correct_streak = 0
            incorrect_streak = np.random.randint(2, 4)
            trend = -1
            current_diff = np.random.randint(2, 4)
            
            training_data.append([accuracy, avg_time, correct_streak, incorrect_streak, trend, current_diff])
            training_labels.append(0)  # Decrease difficulty
        
        # Scenario 3: Average performance (stay same)
        for _ in range(100):
            accuracy = np.random.uniform(50, 75)
            avg_time = np.random.uniform(5, 8)
            correct_streak = np.random.randint(0, 2)
            incorrect_streak = np.random.randint(0, 2)
            trend = 0
            current_diff = np.random.randint(1, 4)
            
            training_data.append([accuracy, avg_time, correct_streak, incorrect_streak, trend, current_diff])
            training_labels.append(1)  # Stay same
        
        # Scenario 4: Mixed performance patterns
        for _ in range(50):
            accuracy = np.random.uniform(60, 85)
            avg_time = np.random.uniform(4, 7)
            correct_streak = np.random.randint(1, 3)
            incorrect_streak = 0
            trend = np.random.choice([-1, 0, 1])
            current_diff = np.random.randint(1, 3)
            
            # Decision based on multiple factors
            if accuracy > 75 and avg_time < 6:
                label = 2
            elif accuracy < 55:
                label = 0
            else:
                label = 1
            
            training_data.append([accuracy, avg_time, correct_streak, incorrect_streak, trend, current_diff])
            training_labels.append(label)
        
        # Train the model
        X_train = np.array(training_data)
        y_train = np.array(training_labels)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Fit model
        self.model.fit(X_train_scaled, y_train)
        
        print("✅ ML Model pretrained with synthetic data")
        print(f"   Training samples: {len(training_data)}")
        print(f"   Model accuracy on training: {self.model.score(X_train_scaled, y_train):.2%}\n")
    
    def _extract_features(self, performance_metrics, current_difficulty):
        """
        Extract features from performance metrics for ML model
        
        Args:
            performance_metrics (dict): Recent performance data
            current_difficulty (int): Current difficulty level
        
        Returns:
            np.array: Feature vector
        """
        features = [
            performance_metrics['accuracy'],
            performance_metrics['avg_time'],
            performance_metrics['correct_streak'],
            performance_metrics['incorrect_streak'],
            performance_metrics['trend'],
            current_difficulty
        ]
        
        return np.array(features).reshape(1, -1)
    
    def update_difficulty(self, performance_metrics, current_difficulty):
        """
        Update difficulty level using ML model (alias for predict_next_difficulty)
        
        Args:
            performance_metrics (dict): Recent performance data
            current_difficulty (int): Current difficulty level (1-3)
        
        Returns:
            int: Updated difficulty level (1-3)
        """
        return self.predict_next_difficulty(performance_metrics, current_difficulty)
    
    def predict_next_difficulty(self, performance_metrics, current_difficulty):
        """
        Predict next difficulty level using ML model
        
        Args:
            performance_metrics (dict): Recent performance data
            current_difficulty (int): Current difficulty level (1-3)
        
        Returns:
            int: Predicted next difficulty level (1-3)
        """
        # If not enough data, use rule-based fallback
        if performance_metrics['recent_problems'] < 2:
            return self._rule_based_fallback(performance_metrics, current_difficulty)
        
        # Extract features
        features = self._extract_features(performance_metrics, current_difficulty)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Get confidence of prediction
        self.last_confidence = np.max(probabilities)
        self.prediction_count += 1
        
        # Map prediction to difficulty
        # 0 = decrease, 1 = stay, 2 = increase
        if prediction == 2:  # Increase
            next_difficulty = min(current_difficulty + 1, 3)
        elif prediction == 0:  # Decrease
            next_difficulty = max(current_difficulty - 1, 1)
        else:  # Stay
            next_difficulty = current_difficulty
        
        # Log prediction (for debugging)
        self._log_prediction(performance_metrics, current_difficulty, next_difficulty, probabilities)
        
        return next_difficulty
    
    def _rule_based_fallback(self, performance_metrics, current_difficulty):
        """
        Simple rule-based system for when ML model doesn't have enough data
        
        Args:
            performance_metrics (dict): Recent performance data
            current_difficulty (int): Current difficulty level
        
        Returns:
            int: Next difficulty level
        """
        accuracy = performance_metrics['accuracy']
        avg_time = performance_metrics['avg_time']
        
        # Simple scoring system
        performance_score = accuracy * 0.7 + max(0, 30 - avg_time) * 0.3
        
        if performance_score > 75 and current_difficulty < 3:
            return current_difficulty + 1
        elif performance_score < 40 and current_difficulty > 1:
            return current_difficulty - 1
        else:
            return current_difficulty
    
    def _log_prediction(self, metrics, current_diff, predicted_diff, probabilities):
        """Log ML predictions for debugging and transparency"""
        print(f"\n🤖 ML Model Prediction #{self.prediction_count}")
        print(f"   Current Difficulty: {current_diff}")
        print(f"   Predicted Difficulty: {predicted_diff}")
        print(f"   Confidence: {self.last_confidence:.2%}")
        print(f"   Probabilities: Decrease={probabilities[0]:.2%}, Stay={probabilities[1]:.2%}, Increase={probabilities[2]:.2%}")
        print(f"   Based on: Accuracy={metrics['accuracy']:.1f}%, Time={metrics['avg_time']:.1f}s, Streak={metrics['correct_streak']}")
    
    def get_model_info(self):
        """Get information about the ML model"""
        return {
            'type': 'Logistic Regression (Multinomial)',
            'classes': ['Decrease Difficulty', 'Stay Same', 'Increase Difficulty'],
            'features': ['Accuracy', 'Avg Time', 'Correct Streak', 'Incorrect Streak', 'Trend', 'Current Difficulty'],
            'predictions_made': self.prediction_count,
            'last_confidence': self.last_confidence
        }


# Testing
if __name__ == "__main__":
    engine = AdaptiveEngine()
    
    print("\n" + "=" * 60)
    print("Testing Adaptive Engine")
    print("=" * 60)
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'High Performer',
            'metrics': {
                'accuracy': 90.0,
                'avg_time': 3.5,
                'correct_streak': 3,
                'incorrect_streak': 0,
                'recent_problems': 3,
                'trend': 1
            },
            'current_diff': 1
        },
        {
            'name': 'Struggling Student',
            'metrics': {
                'accuracy': 33.0,
                'avg_time': 12.0,
                'correct_streak': 0,
                'incorrect_streak': 2,
                'recent_problems': 3,
                'trend': -1
            },
            'current_diff': 3
        },
        {
            'name': 'Average Performance',
            'metrics': {
                'accuracy': 66.0,
                'avg_time': 6.0,
                'correct_streak': 1,
                'incorrect_streak': 0,
                'recent_problems': 3,
                'trend': 0
            },
            'current_diff': 2
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        predicted = engine.predict_next_difficulty(scenario['metrics'], scenario['current_diff'])
        print(f"Result: {scenario['current_diff']} → {predicted}")
    
    print("\n" + "=" * 60)
    print("Model Info:")
    for key, value in engine.get_model_info().items():
        print(f"  {key}: {value}")
