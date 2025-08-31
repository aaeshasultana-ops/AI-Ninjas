import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import datetime

class HealthFoodAdvisor:
    def __init__(self):
        # User profile
        self.user_profile = {
            "name": "",
            "age": 0,
            "weight_kg": 0,
            "height_cm": 0,
            "hba1c": 0,
            "daily_calorie_target": 2000,
            "calories_consumed": 0,
            "steps_today": 0,
            "meals": {
                "breakfast": {"foods": {}, "calories": 0},
                "lunch": {"foods": {}, "calories": 0},
                "dinner": {"foods": {}, "calories": 0},
                "snacks": {"foods": {}, "calories": 0}
            }
        }
        
        # Extensive database of foods with nutritional information (per 100g)
        self.food_database = {
            # Breakfast items
            "idli": {"calories": 39, "carbs": 8, "protein": 2, "fat": 0.5, "category": "breakfast"},
            "dosa": {"calories": 117, "carbs": 18, "protein": 4, "fat": 3.5, "category": "breakfast"},
            "poha": {"calories": 120, "carbs": 25, "protein": 3, "fat": 2, "category": "breakfast"},
            "upma": {"calories": 130, "carbs": 20, "protein": 4, "fat": 4, "category": "breakfast"},
            "oats": {"calories": 150, "carbs": 27, "protein": 5, "fat": 3, "category": "breakfast"},
            "cereal": {"calories": 120, "carbs": 24, "protein": 3, "fat": 1, "category": "breakfast"},
            "sandwich": {"calories": 180, "carbs": 25, "protein": 8, "fat": 5, "category": "breakfast"},
            "paratha": {"calories": 200, "carbs": 25, "protein": 5, "fat": 9, "category": "breakfast"},
            "pancake": {"calories": 150, "carbs": 22, "protein": 4, "fat": 5, "category": "breakfast"},
            "eggs": {"calories": 155, "carbs": 1.1, "protein": 13, "fat": 11, "category": "breakfast"},
            "toast": {"calories": 75, "carbs": 13, "protein": 3, "fat": 1, "category": "breakfast"},
            
            # Main dishes
            "rice": {"calories": 130, "carbs": 28, "protein": 3, "fat": 0.5, "category": "main"},
            "roti": {"calories": 100, "carbs": 20, "protein": 3, "fat": 1, "category": "main"},
            "naan": {"calories": 150, "carbs": 25, "protein": 5, "fat": 4, "category": "main"},
            "pasta": {"calories": 130, "carbs": 25, "protein": 5, "fat": 1, "category": "main"},
            "noodles": {"calories": 140, "carbs": 26, "protein": 4, "fat": 2, "category": "main"},
            "quinoa": {"calories": 120, "carbs": 21, "protein": 4, "fat": 2, "category": "main"},
            "pizza": {"calories": 250, "carbs": 30, "protein": 10, "fat": 10, "category": "main"},
            "burger": {"calories": 300, "carbs": 30, "protein": 15, "fat": 15, "category": "main"},
            
            # Protein sources
            "chicken": {"calories": 165, "carbs": 0, "protein": 31, "fat": 3.6, "category": "protein"},
            "fish": {"calories": 120, "carbs": 0, "protein": 22, "fat": 3, "category": "protein"},
            "paneer": {"calories": 260, "carbs": 4, "protein": 18, "fat": 20, "category": "protein"},
            "tofu": {"calories": 75, "carbs": 2, "protein": 8, "fat": 4, "category": "protein"},
            "dal": {"calories": 120, "carbs": 20, "protein": 8, "fat": 1, "category": "protein"},
            "lentils": {"calories": 115, "carbs": 20, "protein": 9, "fat": 0.4, "category": "protein"},
            "beans": {"calories": 130, "carbs": 23, "protein": 9, "fat": 0.5, "category": "protein"},
            "steak": {"calories": 200, "carbs": 0, "protein": 25, "fat": 12, "category": "protein"},
            
            # Vegetables
            "potato": {"calories": 75, "carbs": 17, "protein": 2, "fat": 0.1, "category": "vegetable"},
            "broccoli": {"calories": 35, "carbs": 7, "protein": 2.5, "fat": 0.5, "category": "vegetable"},
            "carrot": {"calories": 40, "carbs": 9, "protein": 1, "fat": 0.2, "category": "vegetable"},
            "spinach": {"calories": 25, "carbs": 4, "protein": 3, "fat": 0.5, "category": "vegetable"},
            "cabbage": {"calories": 25, "carbs": 6, "protein": 1.5, "fat": 0.1, "category": "vegetable"},
            "cauliflower": {"calories": 25, "carbs": 5, "protein": 2, "fat": 0.5, "category": "vegetable"},
            "salad": {"calories": 30, "carbs": 5, "protein": 1, "fat": 0.5, "category": "vegetable"},
            
            # Snacks
            "vada": {"calories": 155, "carbs": 18, "protein": 5, "fat": 7, "category": "snack"},
            "samosa": {"calories": 250, "carbs": 30, "protein": 5, "fat": 12, "category": "snack"},
            "chips": {"calories": 150, "carbs": 15, "protein": 2, "fat": 9, "category": "snack"},
            "biscuit": {"calories": 100, "carbs": 15, "protein": 2, "fat": 4, "category": "snack"},
            "nuts": {"calories": 180, "carbs": 6, "protein": 5, "fat": 16, "category": "snack"},
            "fruit": {"calories": 60, "carbs": 15, "protein": 1, "fat": 0.5, "category": "snack"},
            "yogurt": {"calories": 60, "carbs": 5, "protein": 4, "fat": 2, "category": "snack"},
            
            # Sweets
            "cake": {"calories": 350, "carbs": 45, "protein": 5, "fat": 16, "category": "dessert"},
            "ice cream": {"calories": 200, "carbs": 25, "protein": 4, "fat": 10, "category": "dessert"},
            "chocolate": {"calories": 220, "carbs": 25, "protein": 3, "fat": 13, "category": "dessert"},
            "cookie": {"calories": 150, "carbs": 20, "protein": 2, "fat": 7, "category": "dessert"},
            
            # Beverages
            "coffee": {"calories": 50, "carbs": 6, "protein": 1, "fat": 2, "category": "beverage"},
            "tea": {"calories": 45, "carbs": 7, "protein": 1, "fat": 1.5, "category": "beverage"},
            "milk": {"calories": 60, "carbs": 5, "protein": 3, "fat": 3, "category": "beverage"},
            "smoothie": {"calories": 120, "carbs": 20, "protein": 5, "fat": 3, "category": "beverage"},
            "juice": {"calories": 100, "carbs": 24, "protein": 1, "fat": 0.5, "category": "beverage"},
            "soda": {"calories": 150, "carbs": 40, "protein": 0, "fat": 0, "category": "beverage"},
        }
        
        # Common synonyms and variations
        self.synonyms = {
            "idly": "idli", "idlis": "idli",
            "masala dosa": "dosa", "plain dosa": "dosa", "dosas": "dosa",
            "medu vada": "vada", "vadas": "vada",
            "chai": "tea", "green tea": "tea",
            "butter milk": "milk", "curd": "yogurt", "yoghurt": "yogurt",
            "pulses": "dal", "legumes": "beans",
            "fries": "potato", "baked potato": "potato", "mashed potato": "potato",
            "fried rice": "rice", "brown rice": "rice", "white rice": "rice",
            "whole wheat bread": "bread", "white bread": "bread", "toasts": "toast",
            "vegetable salad": "salad", "fruit salad": "fruit",
            "paneer curry": "paneer", "chicken curry": "chicken", "fish curry": "fish",
            "orange juice": "juice", "apple juice": "juice", "fruit juice": "juice",
            "cookies": "cookie", "biscuits": "biscuit",
            "almonds": "nuts", "walnuts": "nuts", "peanuts": "nuts"
        }
        
        # Unit words and their multipliers
        self.units = {
            "piece": 1, "pieces": 1, "pc": 1, "pcs": 1,
            "bowl": 2, "bowls": 2,
            "cup": 1.5, "cups": 1.5,
            "plate": 2.5, "plates": 2.5,
            "serving": 2, "servings": 2,
            "small": 0.7, "medium": 1, "large": 1.5,
            "glass": 1.5, "glasses": 1.5,
            "slice": 0.5, "slices": 0.5
        }
        
        # Meal time patterns
        self.meal_patterns = {
            "breakfast": ["breakfast", "morning", "first meal", "early meal"],
            "lunch": ["lunch", "afternoon", "midday", "noon"],
            "dinner": ["dinner", "evening", "night", "supper"],
            "snacks": ["snack", "munch", "bite", "nibble"]
        }
        
        # Food replacement suggestions
        self.replacement_suggestions = {
            "rice": ["quinoa", "cauliflower rice", "steamed vegetables"],
            "pasta": ["zucchini noodles", "spaghetti squash", "shirataki noodles"],
            "bread": ["lettuce wraps", "collard green wraps", "whole grain bread"],
            "potato": ["sweet potato", "cauliflower mash", "turnips"],
            "sugar": ["stevia", "monk fruit", "erythritol"],
            "white flour": ["almond flour", "coconut flour", "whole wheat flour"]
        }
        
        # Protein-rich alternatives
        self.protein_alternatives = ["chicken", "fish", "tofu", "paneer", "eggs", "lentils", "beans", "dal", "yogurt", "nuts"]
        
        # Salad additions
        self.salad_additions = ["spinach", "cabbage", "carrot", "broccoli", "cauliflower", "cucumber", "tomato", "bell pepper"]
        
    def set_user_profile(self, name, age, weight_kg, height_cm, hba1c):
        """Set up user profile and calculate daily calorie target based on HbA1c"""
        self.user_profile["name"] = name
        self.user_profile["age"] = age
        self.user_profile["weight_kg"] = weight_kg
        self.user_profile["height_cm"] = height_cm
        self.user_profile["hba1c"] = hba1c
        
        # Calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor Equation
        if age < 18:
            # For children and teenagers
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            # For adults
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
            if age > 60:
                bmr -= 5  # Adjustment for seniors
        
        # Adjust calorie target based on HbA1c level
        if hba1c < 5.7:
            # Normal HbA1c
            self.user_profile["daily_calorie_target"] = bmr * 1.2  # Sedentary lifestyle
        elif 5.7 <= hba1c <= 6.4:
            # Prediabetes
            self.user_profile["daily_calorie_target"] = bmr * 1.1  # Slightly reduced
        else:
            # Diabetes
            self.user_profile["daily_calorie_target"] = bmr  # Further reduced for better control
    
    def get_ir_sensor_reading(self):
        """Simulate IR sensor reading for glucose monitoring"""
        # In a real application, this would interface with actual hardware
        import random
        return random.randint(70, 200)  # Simulated glucose reading
    
    def set_steps_count(self, steps):
        """Set the step count from smart watch"""
        self.user_profile["steps_today"] = steps
        
        # Adjust calorie target based on activity
        if steps > 10000:
            self.user_profile["daily_calorie_target"] *= 1.2
        elif steps > 5000:
            self.user_profile["daily_calorie_target"] *= 1.1
    
    def extract_meal_type(self, user_input):
        """Extract meal type from natural language input"""
        text = user_input.lower()
        
        for meal_type, patterns in self.meal_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    return meal_type
        
        # If no specific meal type found, try to infer from context
        if "morning" in text or "first" in text:
            return "breakfast"
        elif "afternoon" in text or "midday" in text:
            return "lunch"
        elif "evening" in text or "night" in text:
            return "dinner"
        elif "snack" in text or "munch" in text:
            return "snacks"
            
        return None
    
    def extract_food_items(self, user_input):
        """Extract food items and quantities from natural language input"""
        # Convert to lowercase for easier processing
        text = user_input.lower()
        
        # Replace synonyms with standard names
        for synonym, standard in self.synonyms.items():
            text = re.sub(r'\b' + synonym + r'\b', standard, text)
        
        # Find all mentioned food items
        found_items = []
        for food in self.food_database:
            if re.search(r'\b' + food + r'\b', text):
                found_items.append(food)
        
        # If no direct matches, try partial matches
        if not found_items:
            for food in self.food_database:
                if any(word in text.split() for word in food.split()):
                    found_items.append(food)
        
        # Extract quantities
        food_quantities = {}
        for food in found_items:
            # Look for quantity patterns before the food name
            pattern = r'(\d+)\s*(' + '|'.join(self.units.keys()) + r')?\s*' + food
            match = re.search(pattern, text)
            
            if match:
                quantity = int(match.group(1))
                unit = match.group(2) if match.group(2) else "piece"
                multiplier = self.units.get(unit, 1)
                food_quantities[food] = quantity * multiplier
            else:
                # Check for vague quantity descriptions
                if "some" in text or "a little" in text or "bit of" in text:
                    food_quantities[food] = 0.5
                elif "a lot of" in text or "plenty of" in text:
                    food_quantities[food] = 2
                else:
                    # Default to 1 serving if no quantity specified
                    food_quantities[food] = 1
        
        return food_quantities
    
    def calculate_nutrition(self, food_quantities):
        """Calculate nutritional information based on food quantities"""
        total_nutrition = defaultdict(float)
        breakdown = {}
        
        for food, quantity in food_quantities.items():
            if food in self.food_database:
                nutrition = self.food_database[food]
                breakdown[food] = {
                    "quantity": quantity,
                    "calories": nutrition["calories"] * quantity,
                    "carbs": nutrition["carbs"] * quantity,
                    "protein": nutrition["protein"] * quantity,
                    "fat": nutrition["fat"] * quantity
                }
                
                total_nutrition["calories"] += breakdown[food]["calories"]
                total_nutrition["carbs"] += breakdown[food]["carbs"]
                total_nutrition["protein"] += breakdown[food]["protein"]
                total_nutrition["fat"] += breakdown[food]["fat"]
        
        return total_nutrition, breakdown
    
    def get_meal_replacement_suggestions(self, food_quantities):
        """Generate meal replacement suggestions focusing on protein for carbs and salad additions"""
        suggestions = []
        
        # Check for high-carb foods and suggest protein alternatives
        high_carb_foods = ["rice", "pasta", "bread", "potato", "noodles"]
        for food in food_quantities:
            if food in high_carb_foods:
                # Suggest reducing portion and adding protein
                suggestions.append(f"Consider reducing {food} portion and adding {self.protein_alternatives[0]} or {self.protein_alternatives[1]} for better protein balance.")
                
                # Suggest specific alternatives
                if food in self.replacement_suggestions:
                    alternatives = self.replacement_suggestions[food]
                    suggestions.append(f"You could replace {food} with {alternatives[0]} or {alternatives[1]} for a healthier option.")
        
        # Check if meal lacks vegetables/salad
        vegetable_count = sum(1 for food in food_quantities if self.food_database[food]["category"] in ["vegetable"])
        if vegetable_count < 2:
            suggestions.append(f"Consider adding a salad with {self.salad_additions[0]}, {self.salad_additions[1]}, and {self.salad_additions[2]} for more fiber and nutrients.")
        
        # Check protein content
        protein_foods = [food for food in food_quantities if self.food_database[food]["category"] == "protein"]
        if not protein_foods:
            suggestions.append(f"Your meal could use more protein. Consider adding {self.protein_alternatives[0]}, {self.protein_alternatives[1]}, or {self.protein_alternatives[2]}.")
        
        return suggestions
    
    def get_health_suggestions(self, nutrition_info, meal_type):
        """Generate health suggestions based on meal content and user profile"""
        suggestions = []
        
        # Check carbohydrate content for diabetic users
        if self.user_profile["hba1c"] >= 5.7 and nutrition_info["carbs"] > 30:
            suggestions.append("Your meal is high in carbohydrates. Consider replacing some carbs with protein or vegetables.")
        
        # Check if meal is too high in calories
        remaining_calories = self.user_profile["daily_calorie_target"] - self.user_profile["calories_consumed"]
        if nutrition_info["calories"] > remaining_calories * 0.5:
            suggestions.append("This meal is quite calorie-dense. You might want to consider a lighter option.")
        
        # General health suggestions
        if self.user_profile["steps_today"] < 5000:
            suggestions.append("You haven't reached your step goal today. Try to take a walk after your meal.")
        
        if len(suggestions) == 0:
            suggestions.append("Your meal looks balanced. Keep up the good eating habits!")
        
        return suggestions
    
    def ask_about_previous_meals(self, current_meal):
        """Ask about previous meals based on the current meal"""
        questions = []
        
        if current_meal == "lunch" and not self.user_profile["meals"]["breakfast"]["foods"]:
            questions.append("What did you have for breakfast today?")
        
        if current_meal == "dinner":
            if not self.user_profile["meals"]["breakfast"]["foods"]:
                questions.append("What did you have for breakfast today?")
            if not self.user_profile["meals"]["lunch"]["foods"]:
                questions.append("What did you have for lunch today?")
        
        return questions
    
    def process_meal(self, meal_type, food_quantities):
        """Process a meal and update the user's calorie consumption"""
        total_nutrition, breakdown = self.calculate_nutrition(food_quantities)
        
        # Update meal record
        self.user_profile["meals"][meal_type]["foods"] = breakdown
        self.user_profile["meals"][meal_type]["calories"] = total_nutrition["calories"]
        
        # Update total calories consumed
        self.user_profile["calories_consumed"] += total_nutrition["calories"]
        
        return total_nutrition, breakdown
    
    def get_remaining_calories(self):
        """Calculate remaining calories for the day"""
        return self.user_profile["daily_calorie_target"] - self.user_profile["calories_consumed"]
    
    def generate_response(self, user_input):
        """Generate a natural language response based on user input"""
        # Check if user is asking about IR sensor
        if "sensor" in user_input.lower() or "glucose" in user_input.lower():
            reading = self.get_ir_sensor_reading()
            status = "normal" if 70 <= reading <= 140 else "high" if reading > 140 else "low"
            return f"Your current glucose reading is {reading} mg/dL, which is {status}."
        
        # Check if user is providing step count
        if "steps" in user_input.lower():
            step_match = re.search(r'(\d+)\s*steps?', user_input.lower())
            if step_match:
                steps = int(step_match.group(1))
                self.set_steps_count(steps)
                return f"Thanks for updating your step count to {steps}. I've adjusted your calorie target accordingly."
        
        # Extract meal type from input
        meal_type = self.extract_meal_type(user_input)
        
        if not meal_type:
            return "I'm not sure which meal you're referring to. Could you specify if this is breakfast, lunch, dinner, or a snack?"
        
        # Extract food items from input
        food_quantities = self.extract_food_items(user_input)
        
        if not food_quantities:
            return "I couldn't identify any foods in your message. Could you please specify what you're planning to eat? For example, 'I'm having 2 dosas and a cup of coffee'."
        
        # Process the meal
        total_nutrition, breakdown = self.process_meal(meal_type, food_quantities)
        remaining_calories = self.get_remaining_calories()
        
        # Generate response
        response = f"Okay, I've recorded your {meal_type}:\n\n"
        
        for food, info in breakdown.items():
            response += f"- {info['quantity']} serving(s) of {food}: {info['calories']} calories\n"
        
        response += f"\nTotal for this meal: {total_nutrition['calories']:.1f} calories\n"
        response += f"Daily calorie target: {self.user_profile['daily_calorie_target']:.1f}\n"
        response += f"Calories consumed today: {self.user_profile['calories_consumed']:.1f}\n"
        response += f"Remaining calories: {remaining_calories:.1f}\n\n"
        
        # Add health suggestions
        suggestions = self.get_health_suggestions(total_nutrition, meal_type)
        response += "Health suggestions:\n"
        for i, suggestion in enumerate(suggestions, 1):
            response += f"{i}. {suggestion}\n"
        
        # Add meal replacement suggestions
        replacement_suggestions = self.get_meal_replacement_suggestions(food_quantities)
        if replacement_suggestions:
            response += "\nMeal improvement suggestions:\n"
            for i, suggestion in enumerate(replacement_suggestions, 1):
                response += f"{i}. {suggestion}\n"
        
        # Ask about previous meals if needed
        previous_meal_questions = self.ask_about_previous_meals(meal_type)
        if previous_meal_questions:
            response += "\nTo give you better advice, I need to know about your previous meals:\n"
            for question in previous_meal_questions:
                response += f"- {question}\n"
        
        return response
    
    def list_available_foods(self):
        """Return a list of all available foods in the database"""
        return list(self.food_database.keys())

# Example usage and demonstration
def main():
    advisor = HealthFoodAdvisor()
    
    print("=" * 60)
    print("FOOD NUTRITION ANALYZER WITH HEALTH MONITORING")
    print("=" * 60)
    print("\nHello! I can help you manage your diet and health.")
    
    # Set up user profile
    name = input("What's your name? ")
    age = int(input("How old are you? "))
    weight = float(input("What's your weight in kg? "))
    height = float(input("What's your height in cm? "))
    hba1c = float(input("What's your most recent HbA1c level? "))
    
    advisor.set_user_profile(name, age, weight, height, hba1c)
    
    print(f"\nThanks {name}! Based on your profile, your daily calorie target is {advisor.user_profile['daily_calorie_target']:.0f} calories.")
    
    # Ask for step count
    steps_input = input("How many steps have you taken today? (Press Enter if you don't know) ")
    if steps_input.isdigit():
        advisor.set_steps_count(int(steps_input))
        print(f"Thanks! I've noted your step count of {steps_input}.")
    
    print("\nYou can describe your meals in natural language, for example:")
    print("- 'I had 2 idlis and a vada for breakfast'")
    print("- 'For lunch, I'm planning to have rice with dal and vegetables'")
    print("- 'I just had a small snack with some fruits'")
    print("- 'What's my current glucose level?'")
    print("- 'I walked 7500 steps today'")
    print("\nType 'quit' to exit the program.\n")
    
    while True:
        user_input = input("What would you like to tell me about your meals? ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print(f"Thank you for using the Health Food Advisor, {name}. Stay healthy!")
            break
        
        response = advisor.generate_response(user_input)
        print("\n" + response + "\n")

if __name__ == "__main__":
    main()