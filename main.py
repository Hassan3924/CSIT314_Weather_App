import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def cleaningDataScreen():
    loading_window = tk.Toplevel(root)
    loading_window.geometry("200x100")
    data_clean()
    loading_label = tk.Label(loading_window, text="Cleaning the data...")
    loading_label.pack(pady=20)
    root.after(2000, loading_window.destroy)

def collectingDataScreen():
    loading_window = tk.Toplevel(root)
    loading_window.geometry("200x100")
    loading_label = tk.Label(loading_window, text="Collecting data...")
    loading_label.pack(pady=20)
    def destroy_and_clean():
        loading_window.destroy()
        cleaningDataScreen()
    root.after(2000, destroy_and_clean)  # this function will destroy the window and call cleaningDataScreen


def data_clean():
    df = pd.read_csv('Weather_Data.csv')
    df = df.drop(["Evaporation", "Humidity9am", "Humidity3pm", "Cloud9am", "Cloud3pm"], axis = 1)
    for label, content in df.items():
        if pd.api.types.is_numeric_dtype(content):
            if pd.isnull(content).sum():
                # Filling missing data
                df[label] = content.fillna(content.median())

    df["RainTomorrow"] = df["RainTomorrow"].replace({0: "No", 1: "Yes"})
    df.to_csv("Cleaned_Weather_Data_2.csv", index= False)

def show_analysis():
    # Load the cleaned data
    df = pd.read_csv("Cleaned_Weather_Data_2.csv")
    df['RainTodayLabeled'] = df['RainToday'].map({'Yes': 1, 'No': 0})

    # Plot WindSpeed9am vs Pressure9am

    plt.figure(figsize=(10, 5))
    plt.scatter(df['WindSpeed9am'], df['Pressure9am'])
    plt.title('WindSpeed9am vs Pressure9am')
    plt.xlabel('WindSpeed9am')
    plt.ylabel('Pressure9am')
    plt.show()

    # Plot WindSpeed3pm vs Pressure3pm
    plt.figure(figsize=(10, 5))
    plt.scatter(df['WindSpeed3pm'], df['Pressure3pm'])
    plt.title('WindSpeed3pm vs Pressure3pm')
    plt.xlabel('WindSpeed3pm')
    plt.ylabel('Pressure3pm')
    plt.show()

    # Group data by location and calculate the sum of the Rainfall for each group
    rainfall_by_location = df.groupby('Location')['Rainfall'].sum()

    # Sort the data in descending order
    rainfall_by_location = rainfall_by_location.sort_values(ascending=False)

    # Create the bar plot
    plt.figure(figsize=(10, 8))
    rainfall_by_location.plot(kind='bar')
    plt.xlabel('Location')
    plt.ylabel('Total Rainfall')
    plt.title('Total Rainfall by Location')

    # Show the plot
    plt.show()

    # Create a new DataFrame with just the variables of interest
    selected_data = df[['WindSpeed9am', 'WindSpeed3pm', 'Temp9am', 'Temp3pm', 'RainToday', 'RainTomorrow']].copy()

    # Handle categorical variables (assuming 'Yes' for rain and 'No' for no rain)
    selected_data.loc[:, 'RainToday'] = selected_data['RainToday'].map({'Yes': 1, 'No': 0})
    selected_data.loc[:, 'RainTomorrow'] = selected_data['RainTomorrow'].map({'Yes': 1, 'No': 0})

    # Use seaborn to create a pair plot
    sns.pairplot(selected_data, hue='RainToday', palette='coolwarm')

    # Show the plot
    plt.show()


root = tk.Tk(className="Weatherly")
root.geometry("700x400")

frame = ttk.Frame(root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ttk.Label(frame, text="Weatherly", font=("Roboto", 24))
label.pack(pady=12, padx=10)

button_frame = ttk.Frame(frame)  # Create a new frame for the button
button_frame.pack(fill='x')  # Use pack to add the new frame to the main frame

style = ttk.Style()
style.configure('Big.TButton', font=('Arial', 15), padding=15)

dataCleaning = ttk.Button(button_frame, text="Collect Data", style='Big.TButton', command=collectingDataScreen)
dataCleaning.grid(row=0, column=0, padx=25, sticky='w')

showAnalysis = ttk.Button(button_frame, text="Show Analysis", style='Big.TButton', command =show_analysis )
showAnalysis.grid(row=0, column=0, padx=400, sticky='w')

root.mainloop()
