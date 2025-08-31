import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler

class GlucosePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_data(self):
        """Prepare the training dataset"""
        # Little finger data
        little_finger_readings = [163.5,166.5,162.5,164.5,160.5,165.5,164.5,164.5,164.5,166.5,
                                169.5,180.5,166.5,164.5,164.5,165.5,166.5,166.5,163.4,166.5]
        little_finger_glucose = [90,95,114,153,169,221,91,139,89,220,
                               190,165,100,121,90,210,99,145,128,211]
        
        # Thumb data
        thumb_readings = [163.5,162.5,196.5,186,189.5,180.5,184.5,180,182,180,
                        187.5,189.5,183,185,181.5,180.5,185,185,180,185]
        thumb_glucose = [90,95,114,153,169,221,91,139,89,220,
                        190,165,100,121,90,210,99,145,128,211]
        
        # Combine both datasets
        all_readings = little_finger_readings + thumb_readings
        all_glucose = little_finger_glucose + thumb_glucose
        finger_type = ['little'] * len(little_finger_readings) + ['thumb'] * len(thumb_readings)
        
        # Create DataFrame
        df = pd.DataFrame({
            'sensor_reading': all_readings,
            'glucose_level': all_glucose,
            'finger_type': finger_type
        })
        
        return df
    
    def train_model(self):
        """Train the machine learning model"""
        # Prepare data
        df = self.prepare_data()
        
        # Prepare features and target
        X = df[['sensor_reading']].values
        y = df['glucose_level'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train multiple models
        models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Linear Regression': LinearRegression()
        }
        
        best_model = None
        best_score = -np.inf
        best_model_name = ""
        
        print("Training models...")
        print("=" * 50)
        
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = r2_score(y_test, y_pred)
            
            print(f"{name}:")
            print(f"  R² Score: {score:.4f}")
            print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
            print(f"  MAE: {mean_absolute_error(y_test, y_pred):.2f}")
            print("-" * 30)
            
            if score > best_score:
                best_score = score
                best_model = model
                best_model_name = name
        
        self.model = best_model
        self.is_trained = True
        
        print(f"Selected best model: {best_model_name}")
        print(f"Best R² Score: {best_score:.4f}")
        
        # Plot the results
        self.plot_results(df)
        
        return best_score
    
    def predict_glucose(self, sensor_reading, finger_type='little'):
        """Predict glucose level from sensor reading"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare input
        reading_array = np.array([[sensor_reading]])
        reading_scaled = self.scaler.transform(reading_array)
        
        # Make prediction
        prediction = self.model.predict(reading_scaled)[0]
        
        return round(prediction, 1)
    
    def plot_results(self, df):
        """Plot the training results and regression line"""
        X = df[['sensor_reading']].values
        X_scaled = self.scaler.transform(X)
        y_pred = self.model.predict(X_scaled)
        
        plt.figure(figsize=(12, 6))
        
        # Plot actual data points
        colors = {'little': 'blue', 'thumb': 'red'}
        for finger in df['finger_type'].unique():
            mask = df['finger_type'] == finger
            plt.scatter(df.loc[mask, 'sensor_reading'], 
                       df.loc[mask, 'glucose_level'], 
                       color=colors[finger], 
                       alpha=0.7, 
                       label=f'{finger} finger',
                       s=80)
        
        # Plot regression line
        X_plot = np.linspace(df['sensor_reading'].min(), df['sensor_reading'].max(), 100).reshape(-1, 1)
        X_plot_scaled = self.scaler.transform(X_plot)
        y_plot = self.model.predict(X_plot_scaled)
        
        plt.plot(X_plot, y_plot, 'black', linewidth=2, label='Regression Line')
        
        plt.xlabel('IR Sensor Reading')
        plt.ylabel('Glucose Level (mg/dL)')
        plt.title('Glucose Level vs IR Sensor Reading\n(Prediction Model)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Add correlation coefficient
        correlation = df['sensor_reading'].corr(df['glucose_level'])
        plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def interactive_prediction(self):
        """Interactive mode for glucose prediction"""
        if not self.is_trained:
            print("Training model first...")
            self.train_model()
        
        print("\n" + "=" * 60)
        print("GLUCOSE PREDICTION SYSTEM")
        print("=" * 60)
        print("Trained on IR sensor readings vs glucose levels")
        print(f"Dataset size: 40 samples (20 little finger + 20 thumb)")
        print("=" * 60)
        
        while True:
            try:
                print("\nOptions:")
                print("1. Predict glucose level")
                print("2. Show model information")
                print("3. Exit")
                
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == '1':
                    # Get sensor reading input
                    sensor_input = input("Enter IR sensor reading: ").strip()
                    
                    if sensor_input.lower() == 'exit':
                        break
                    
                    sensor_reading = float(sensor_input)
                    
                    # Get finger type
                    print("\nFinger type:")
                    print("1. Little finger")
                    print("2. Thumb")
                    finger_choice = input("Select finger type (1-2, default=1): ").strip()
                    
                    finger_type = 'little'
                    if finger_choice == '2':
                        finger_type = 'thumb'
                    
                    # Make prediction
                    prediction = self.predict_glucose(sensor_reading, finger_type)
                    
                    print(f"\n🔮 PREDICTION RESULTS:")
                    print("=" * 30)
                    print(f"IR Sensor Reading: {sensor_reading}")
                    print(f"Finger Type: {finger_type}")
                    print(f"Predicted Glucose Level: {prediction} mg/dL")
                    print("=" * 30)
                    
                    # Provide interpretation
                    if prediction < 70:
                        print("⚠️  Warning: Predicted hypoglycemia (low blood sugar)")
                    elif prediction > 180:
                        print("⚠️  Warning: Predicted hyperglycemia (high blood sugar)")
                    else:
                        print("✅ Predicted glucose level within normal range")
                
                elif choice == '2':
                    self.show_model_info()
                
                elif choice == '3' or choice.lower() == 'exit':
                    print("Thank you for using the Glucose Prediction System!")
                    break
                
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            
            except ValueError:
                print("Please enter a valid number for sensor reading.")
            except Exception as e:
                print(f"Error: {e}")
    
    def show_model_info(self):
        """Display model information"""
        if not self.is_trained:
            print("Model not trained yet.")
            return
        
        df = self.prepare_data()
        
        print("\n📊 MODEL INFORMATION:")
        print("=" * 40)
        print(f"Dataset Statistics:")
        print(f"  Total samples: {len(df)}")
        print(f"  Little finger samples: {len(df[df['finger_type'] == 'little'])}")
        print(f"  Thumb samples: {len(df[df['finger_type'] == 'thumb'])}")
        print(f"  Sensor reading range: {df['sensor_reading'].min():.1f} - {df['sensor_reading'].max():.1f}")
        print(f"  Glucose level range: {df['glucose_level'].min()} - {df['glucose_level'].max()} mg/dL")
        print(f"  Correlation coefficient: {df['sensor_reading'].corr(df['glucose_level']):.3f}")
        print("\nThe model predicts glucose levels based on IR sensor readings.")
        print("Note: This is a predictive model and should not replace medical devices.")

    def test_predictions(self):
        """Test the model with sample readings"""
        if not self.is_trained:
            print("Training model first...")
            self.train_model()
        
        print("\n🧪 SAMPLE PREDICTIONS:")
        print("=" * 40)
        
        # Test with various sensor readings
        test_readings = [130, 135, 140, 145, 150, 155, 160, 165]
        
        for reading in test_readings:
            prediction = self.predict_glucose(reading)
            print(f"Sensor: {reading} -> Predicted Glucose: {prediction} mg/dL")

# Main execution
def main():
    """Main function to run the glucose prediction system"""
    try:
        # Create predictor instance
        predictor = GlucosePredictor()
        
        # Train the model
        print("Initializing Glucose Prediction System...")
        predictor.train_model()
        
        # Start interactive prediction
        predictor.interactive_prediction()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()