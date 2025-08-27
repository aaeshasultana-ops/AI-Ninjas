import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json

class NutritionAdvisor:
    def __init__(self):
        # Nutritional database (simplified)
        self.food_db = {
            'apple': {'carbs': 25, 'protein': 0.5, 'fat': 0.3, 'glycemic_index': 36},
            'banana': {'carbs': 27, 'protein': 1.3, 'fat': 0.4, 'glycemic_index': 51},
            'chicken breast': {'carbs': 0, 'protein': 31, 'fat': 3.6, 'glycemic_index': 0},
            'brown rice': {'carbs': 45, 'protein': 5, 'fat': 1.8, 'glycemic_index': 55},
            'avocado': {'carbs': 9, 'protein': 2, 'fat': 15, 'glycemic_index': 15},
            'whole wheat bread': {'carbs': 49, 'protein': 13, 'fat': 4, 'glycemic_index': 71},
            'salmon': {'carbs': 0, 'protein': 25, 'fat': 13, 'glycemic_index': 0},
            'broccoli': {'carbs': 7, 'protein': 2.8, 'fat': 0.4, 'glycemic_index': 15},
            'greek yogurt': {'carbs': 6, 'protein': 10, 'fat': 5, 'glycemic_index': 35},
            'quinoa': {'carbs': 39, 'protein': 8, 'fat': 4, 'glycemic_index': 53}
        }
        
        self.user_data = {
            'steps': 0,
            'calories_burned': 0,
            'meal_history': []
        }
    
    def get_user_input(self):
        """Get food input from user"""
        print("🍽️  Nutrition Advisor - Meal Analysis System")
        print("=" * 50)
        
        food_input = input("Please enter the foods you're planning to eat (comma-separated): ")
        foods = [food.strip().lower() for food in food_input.split(',')]
        
        return foods
    
    def get_smartwatch_data(self):
        """Simulate smartwatch data extraction"""
        print("\n⌚ Smart Watch Data Integration")
        print("-" * 30)
        
        # In real implementation, this would connect to smartwatch API
        steps = int(input("Enter number of steps from your smartwatch: "))
        calories = int(input("Enter calories burned today: "))
        
        self.user_data['steps'] = steps
        self.user_data['calories_burned'] = calories
        
        return steps, calories
    
    def analyze_nutrition(self, foods):
        """Analyze nutritional content of selected foods"""
        total_nutrition = {
            'carbs': 0, 'protein': 0, 'fat': 0, 
            'glycemic_load': 0, 'calories': 0
        }
        
        found_foods = []
        missing_foods = []
        
        for food in foods:
            if food in self.food_db:
                nutrition = self.food_db[food]
                total_nutrition['carbs'] += nutrition['carbs']
                total_nutrition['protein'] += nutrition['protein']
                total_nutrition['fat'] += nutrition['fat']
                total_nutrition['glycemic_load'] += nutrition['glycemic_index'] * nutrition['carbs'] / 100
                total_nutrition['calories'] += (nutrition['carbs'] * 4 + 
                                              nutrition['protein'] * 4 + 
                                              nutrition['fat'] * 9)
                found_foods.append(food)
            else:
                missing_foods.append(food)
        
        return total_nutrition, found_foods, missing_foods
    
    def calculate_recommendations(self, nutrition, steps, calories_burned):
        """Generate personalized recommendations"""
        recommendations = {
            'additions': [],
            'deletions': [],
            'replacements': [],
            'general': []
        }
        
        # Activity-based adjustments
        activity_level = 'sedentary'
        if steps > 10000:
            activity_level = 'very_active'
            protein_target = 80
            carb_target = 150
        elif steps > 7000:
            activity_level = 'active'
            protein_target = 70
            carb_target = 130
        else:
            activity_level = 'sedentary'
            protein_target = 60
            carb_target = 100
        
        # Macronutrient analysis
        if nutrition['protein'] < protein_target:
            recommendations['additions'].extend([
                'Add lean protein sources: chicken breast, fish, tofu, or Greek yogurt',
                f'Current protein: {nutrition["protein"]}g, Target: {protein_target}g'
            ])
        
        if nutrition['carbs'] > carb_target + 30:
            recommendations['deletions'].append(
                f'Consider reducing carbohydrates. Current: {nutrition["carbs"]}g'
            )
        
        # Glycemic index analysis
        if nutrition['glycemic_load'] > 50:
            recommendations['replacements'].append(
                'Replace high-GI foods with low-GI alternatives'
            )
        
        # General health recommendations
        if steps < 5000:
            recommendations['general'].append(
                'Low activity level detected. Consider adding a walk after meals'
            )
        
        return recommendations, activity_level
    
    def suggest_meal_modifications(self, foods, nutrition):
        """Suggest specific food modifications"""
        modifications = []
        
        # High GI food replacements
        high_gi_foods = {'white bread', 'white rice', 'potato', 'sugar'}
        for food in foods:
            if food in high_gi_foods:
                modifications.append(
                    f"Replace {food} with lower GI alternative"
                )
        
        # Protein optimization
        if nutrition['protein'] < 50:
            modifications.append(
                "Add protein source: chicken, fish, eggs, or legumes"
            )
        
        # Healthy fats
        if nutrition['fat'] < 20:
            modifications.append(
                "Add healthy fats: avocado, nuts, or olive oil"
            )
        
        return modifications
    
    def generate_meal_plan(self, foods, recommendations):
        """Generate optimized meal plan"""
        print("\n📋 Optimized Meal Plan Suggestions")
        print("=" * 40)
        
        # Current meal analysis
        print(f"\nCurrent meal items: {', '.join(foods)}")
        
        # Suggested additions
        if recommendations['additions']:
            print("\n➕ Suggested Additions:")
            for addition in recommendations['additions']:
                print(f"  - {addition}")
        
        # Suggested deletions/replacements
        if recommendations['deletions']:
            print("\n➖ Suggested Reductions:")
            for deletion in recommendations['deletions']:
                print(f"  - {deletion}")
        
        if recommendations['replacements']:
            print("\n🔄 Suggested Replacements:")
            for replacement in recommendations['replacements']:
                print(f"  - {replacement}")
    
    def run(self):
        """Main execution function"""
        try:
            # Get user input
            foods = self.get_user_input()
            
            # Get smartwatch data
            steps, calories_burned = self.get_smartwatch_data()
            
            # Analyze nutrition
            nutrition, found_foods, missing_foods = self.analyze_nutrition(foods)
            
            # Generate recommendations
            recommendations, activity_level = self.calculate_recommendations(
                nutrition, steps, calories_burned
            )
            
            # Display results
            print(f"\n📊 Nutritional Analysis")
            print("=" * 30)
            print(f"Total Carbohydrates: {nutrition['carbs']}g")
            print(f"Total Protein: {nutrition['protein']}g")
            print(f"Total Fat: {nutrition['fat']}g")
            print(f"Estimated Calories: {nutrition['calories']} kcal")
            print(f"Glycemic Load: {nutrition['glycemic_load']:.1f}")
            print(f"Activity Level: {activity_level.title()}")
            
            # Generate meal plan suggestions
            self.generate_meal_plan(found_foods, recommendations)
            
            # Show missing foods
            if missing_foods:
                print(f"\n⚠️  Foods not in database: {', '.join(missing_foods)}")
            
            print(f"\n🎯 Based on your {steps} steps and {calories_burned} calories burned")
            
        except Exception as e:
            print(f"Error: {e}")

# Run the system
if __name__ == "__main__":
    advisor = NutritionAdvisor()
    advisor.run()