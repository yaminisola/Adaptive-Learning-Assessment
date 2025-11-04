# 🧮 Math Adventures - AI-Powered Adaptive Learning System

An intelligent math learning system that uses **Machine Learning (Logistic Regression)** to dynamically adjust problem difficulty based on student performance in real-time.

## 📋 Overview

This prototype demonstrates how AI can personalize education by keeping learners in their optimal challenge zone - not too easy (boring) and not too hard (frustrating).

### Key Features
- ✨ **ML-Powered Adaptation**: Uses Logistic Regression to predict optimal difficulty
- 📊 **Real-time Performance Tracking**: Monitors accuracy, speed, and learning trends
- 🎯 **3 Difficulty Levels**: Easy, Medium, and Hard with progressive complexity
- 📈 **Comprehensive Analytics**: Detailed session summaries and recommendations
- 🤖 **Transparent AI**: Shows model confidence and reasoning for each adjustment

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Student   │─────▶│ Puzzle Generator │─────▶│  Math Problem   │
└─────────────┘      └──────────────────┘      └─────────────────┘
       │                                                 │
       │ Answer + Time                                  │
       ▼                                                 ▼
┌─────────────────┐                            ┌─────────────────┐
│ Performance     │◀───────────────────────────│   Evaluation    │
│ Tracker         │                            └─────────────────┘
└─────────────────┘
       │
       │ Recent Performance Data
       ▼
┌─────────────────────────────────────────────────┐
│          Adaptive Engine (ML Model)             │
│  • Logistic Regression (Multinomial)            │
│  • Features: accuracy, time, streaks, trend     │
│  • Predicts: Increase/Stay/Decrease difficulty  │
└─────────────────────────────────────────────────┘
       │
       │ Next Difficulty Level
       ▼
┌─────────────────┐
│  Next Problem   │
└─────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/math-adaptive-learning.git
cd math-adaptive-learning

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python src/main.py
```

## 📂 Project Structure

```
math-adaptive-learning/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── src/
│   ├── main.py              # Main application entry point
│   ├── puzzle_generator.py  # Generates math problems
│   ├── tracker.py           # Tracks performance metrics
│   └── adaptive_engine.py   # ML-based difficulty adaptation
└── docs/
    └── technical_note.pdf   # Detailed technical documentation
```

## 🧠 How the ML Model Works

### Model: Logistic Regression (Multinomial Classification)

**Input Features (6 dimensions):**
1. **Accuracy (%)**: Percentage of correct answers in recent problems
2. **Average Time (seconds)**: Speed of responses
3. **Correct Streak**: Number of consecutive correct answers
4. **Incorrect Streak**: Number of consecutive incorrect answers
5. **Trend**: Performance direction (-1 declining, 0 stable, 1 improving)
6. **Current Difficulty**: Current problem difficulty level (1-3)

**Output Classes (3 decisions):**
- **Class 0**: Decrease difficulty (student struggling)
- **Class 1**: Stay at current difficulty (optimal challenge)
- **Class 2**: Increase difficulty (student excelling)

### Training Strategy

The model is **pre-trained** with synthetic data representing:
- 100 high-performing students (80-100% accuracy, fast responses) → Increase difficulty
- 100 struggling students (0-40% accuracy, slow responses) → Decrease difficulty
- 100 average students (50-75% accuracy, moderate speed) → Stay same
- 50 mixed performance patterns → Context-dependent decisions

This allows the system to work immediately without needing real student data.

### Decision Example

**Scenario**: Student with 90% accuracy, 3.5s average time, 3-problem correct streak
- **Features**: [90.0, 3.5, 3, 0, 1, 1] → scaled to [-1.2, 0.8, 1.5, -0.3, 1.0, -1.0]
- **Model Prediction**: Class 2 (Increase) with 85% confidence
- **Action**: Difficulty 1 → 2 (Easy → Medium)
- **Reasoning**: High accuracy + fast time + positive trend = ready for challenge

## 📊 Metrics Tracked

### Individual Problem Level
- Correctness (✓/✗)
- Response time (seconds)
- Difficulty level attempted
- User answer vs. correct answer

### Session Level
- Total accuracy percentage
- Average response time
- Problems solved per difficulty
- Number of difficulty adjustments
- Performance trend analysis

### ML Model Metrics
- Prediction confidence scores
- Feature importance
- Decision probabilities
- Model accuracy on training data

## 🎯 Difficulty Levels Explained

| Level | Name   | Operations | Number Range | Example |
|-------|--------|-----------|--------------|---------|
| 1     | Easy   | +, -      | 1-10         | 5 + 3 = ? |
| 2     | Medium | +, -, ×   | 1-20         | 15 × 4 = ? |
| 3     | Hard   | +, -, ×, ÷ | 5-50        | 48 ÷ 6 = ? |

## 🔬 Testing the System

### Run Individual Modules

```bash
# Test Puzzle Generator
python src/puzzle_generator.py

# Test Performance Tracker
python src/tracker.py

# Test Adaptive Engine
python src/adaptive_engine.py
```

### Sample Output

```
🤖 ML Model Prediction #3
   Current Difficulty: 1
   Predicted Difficulty: 2
   Confidence: 85.23%
   Probabilities: Decrease=5.12%, Stay=9.65%, Increase=85.23%
   Based on: Accuracy=100.0%, Time=3.2s, Streak=3
```

## 📈 Future Improvements

### Data Collection Strategy
1. **Phase 1 (Month 1-3)**: Deploy to 100 students, collect real performance data
2. **Phase 2 (Month 4-6)**: Retrain model with actual student data
3. **Phase 3 (Month 7+)**: Implement continuous learning from all users

### Advanced Features
- [ ] **Deep Learning**: LSTM for sequence prediction of performance patterns
- [ ] **Reinforcement Learning**: Q-learning for optimal difficulty paths
- [ ] **Multi-topic Support**: Extend to fractions, geometry, word problems
- [ ] **Personalization**: Individual student profiles and learning curves
- [ ] **Explainable AI**: Visualize why model makes each decision

## 🤔 Discussion Questions

### 1. Handling Noisy/Inconsistent Performance
**Problem**: Student randomly guesses or has inconsistent focus

**Solutions**:
- Use larger sliding windows (5-7 problems instead of 3)
- Add response time thresholds (too fast = likely guessing)
- Implement confidence scoring (penalize very fast incorrect answers)
- Smooth transitions (require 2 consecutive signals before changing)

### 2. Rule-Based vs. ML Trade-offs

| Aspect | Rule-Based | Machine Learning |
|--------|-----------|------------------|
| Interpretability | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐ Moderate |
| Personalization | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ High |
| Cold Start | ⭐⭐⭐⭐⭐ Works immediately | ⭐⭐ Needs data |
| Maintenance | ⭐⭐⭐ Manual tuning | ⭐⭐⭐⭐ Self-improving |
| Complexity | ⭐⭐ Simple | ⭐⭐⭐⭐ Complex |

**Hybrid Approach** (our implementation):
- Use ML for prediction with rule-based fallback
- Get benefits of both: immediate functionality + learning capability

### 3. Scaling to Different Topics

**Math → Reading Comprehension**
```python
# Similar architecture, different puzzle generation
def generate_reading_puzzle(difficulty):
    if difficulty == 1:
        return short_passage() + simple_questions(3)
    elif difficulty == 2:
        return medium_passage() + inference_questions(5)
    else:
        return complex_passage() + analysis_questions(8)
```

**Key Insight**: Adaptive engine stays the same! Only puzzle generator changes.

## 🏆 Why This Approach Works

1. **Keeps Students Engaged**: Problems match current skill level
2. **Builds Confidence**: Gradual progression prevents frustration
3. **Identifies Struggles Early**: ML detects declining performance quickly
4. **Personalized Pacing**: Fast learners accelerate, others get more practice
5. **Data-Driven**: Decisions based on actual performance, not assumptions
<img width="948" height="889" alt="image" src="https://github.com/user-attachments/assets/3aba4617-859f-4e26-9c7b-07c22ad6e28c" />

<img width="1584" height="883" alt="image" src="https://github.com/user-attachments/assets/085e51d9-c83b-4de5-af94-6ff56d519e7c" />
