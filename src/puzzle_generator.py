import random


class PuzzleGenerator:
    """Generates math puzzles at different difficulty levels"""
    
    def __init__(self):
        self.operations = ['+', '-', '*', '/']
    
    def generate_puzzle(self, difficulty):
        """
        Generate a math puzzle based on difficulty level
        
        Args:
            difficulty (int): 1 (Easy), 2 (Medium), or 3 (Hard)
        
        Returns:
            dict: Puzzle with num1, num2, operation, and answer
        """
        if difficulty == 1:
            return self._generate_easy()
        elif difficulty == 2:
            return self._generate_medium()
        else:
            return self._generate_hard()
    
    def _generate_easy(self):
        """
        Easy difficulty:
        - Operations: Addition and Subtraction only
        - Number range: 1-10
        - No negative results
        """
        operation = random.choice(['+', '-'])
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        
        # Ensure no negative results for subtraction
        if operation == '-' and num2 > num1:
            num1, num2 = num2, num1
        
        answer = self._calculate(num1, num2, operation)
        
        return {
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'answer': answer,
            'difficulty': 1
        }
    
    def _generate_medium(self):
        """
        Medium difficulty:
        - Operations: Addition, Subtraction, Multiplication
        - Number range: 1-20 for addition/subtraction, 1-12 for multiplication
        - No negative results
        """
        operation = random.choice(['+', '-', '*'])
        
        if operation == '*':
            # Times tables (1-12)
            num1 = random.randint(2, 12)
            num2 = random.randint(2, 12)
        else:
            # Addition and subtraction with larger numbers
            num1 = random.randint(10, 20)
            num2 = random.randint(1, 10)
            
            # Ensure no negative results for subtraction
            if operation == '-' and num2 > num1:
                num1, num2 = num2, num1
        
        answer = self._calculate(num1, num2, operation)
        
        return {
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'answer': answer,
            'difficulty': 2
        }
    
    def _generate_hard(self):
        """
        Hard difficulty:
        - Operations: All four operations
        - Number range: 20-50 for add/sub, 5-15 for mult, controlled division
        - Division results in whole numbers
        """
        operation = random.choice(self.operations)
        
        if operation == '*':
            # Larger multiplication
            num1 = random.randint(5, 15)
            num2 = random.randint(5, 15)
        elif operation == '/':
            # Generate division that results in whole numbers
            num2 = random.randint(2, 12)
            quotient = random.randint(5, 15)
            num1 = num2 * quotient
        elif operation == '-':
            # Subtraction with larger numbers
            num1 = random.randint(20, 50)
            num2 = random.randint(5, 20)
            if num2 > num1:
                num1, num2 = num2, num1
        else:  # Addition
            num1 = random.randint(20, 50)
            num2 = random.randint(10, 30)
        
        answer = self._calculate(num1, num2, operation)
        
        return {
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'answer': answer,
            'difficulty': 3
        }
    
    def _calculate(self, num1, num2, operation):
        """Calculate the answer for a given operation"""
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            return num1 / num2
        else:
            raise ValueError(f"Unknown operation: {operation}")


# Testing
if __name__ == "__main__":
    generator = PuzzleGenerator()
    
    print("Testing Puzzle Generator\n")
    print("=" * 50)
    
    for difficulty in [1, 2, 3]:
        difficulty_names = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
        print(f"\n{difficulty_names[difficulty]} Puzzles:")
        print("-" * 50)
        
        for i in range(5):
            puzzle = generator.generate_puzzle(difficulty)
            print(f"{puzzle['num1']} {puzzle['operation']} {puzzle['num2']} = {puzzle['answer']}")
    
    print("\n" + "=" * 50)
