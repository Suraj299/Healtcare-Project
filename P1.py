import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import speech_recognition as sr
import csv
import sqlite3

# Function to initialize the recognizer and capture voice input
def get_voice_input(question):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(question)
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening... Please speak now.")
        
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}\n")
            return text
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            messagebox.showerror("Error", "Speech service is unavailable. Please check your connection.")
            return ""

def fill_field(entry, question):
    # Capture voice input and fill the entry field
    voice_text = get_voice_input(question)
    if voice_text:
        entry.delete(0, tk.END)  # Clear current text in the entry field
        entry.insert(0, voice_text)  # Insert the captured voice text

def save_to_csv(data):
    with open("healthcare_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to save data to the database
def save_to_database(data):
    conn = sqlite3.connect("healthcare_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS healthcare_records (
            S_NO INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, age TEXT, gender TEXT, contact TEXT,
            symptoms TEXT, duration TEXT, medication TEXT, follow_up TEXT
        )
    """)
    cursor.execute("INSERT INTO healthcare_records (name, age, gender, contact, symptoms, duration, medication, follow_up) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

# Function to display the collected information, save to CSV, and database
def display_summary():
    summary = (
        f"Name: {name_entry.get()}\n"
        f"Age: {age_entry.get()}\n"
        f"Gender: {gender_entry.get()}\n"
        f"Contact Number: {contact_entry.get()}\n"
        f"Symptoms: {symptoms_entry.get()}\n"
        f"Duration: {duration_entry.get()}\n"
        f"Medications: {medication_entry.get()}\n"
        f"Follow-up Appointment: {follow_up_entry.get()}"
    )
    messagebox.showinfo("Form Summary", summary)

    # Save data to CSV and database
    data = [
        name_entry.get(),
        age_entry.get(),
        gender_entry.get(),
        contact_entry.get(),
        symptoms_entry.get(),
        duration_entry.get(),
        medication_entry.get(),
        follow_up_entry.get(),
    ]
    save_to_csv(data)
    save_to_database(data)
    messagebox.showinfo("Success", "Data saved successfully!")

# Function to clear all input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    symptoms_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    medication_entry.delete(0, tk.END)
    follow_up_entry.delete(0, tk.END)

# Function to view data from the database in a table format
def view_database():
    # Connect to the SQLite database
    conn = sqlite3.connect("healthcare_data.db")
    cursor = conn.cursor()
    
    # Fetch all rows from the healthcare_records table
    cursor.execute("SELECT * FROM healthcare_records")
    records = cursor.fetchall()
    
    # Close the database connection
    conn.close()

    # Create a new window to display the data
    view_window = tk.Toplevel(root)
    view_window.title("Database Records")
    view_window.geometry("950x400")
    
    # Create a Treeview widget to display data in a table format
    tree = ttk.Treeview(view_window, columns=("S.NO.", "Name", "Age", "Gender", "Contact", "Symptoms", "Duration", "Medications", "Follow-up"), show="headings")
    
    # Define column headings
    tree.heading("S.NO.", text="S.NO.")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Contact", text="Contact")
    tree.heading("Symptoms", text="Symptoms")
    tree.heading("Duration", text="Duration")
    tree.heading("Medications", text="Medications")
    tree.heading("Follow-up", text="Follow-up")
    
    # Set the style for the Treeview headers
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    # Define column width and alignment
    for col in ("S.NO.", "Name", "Age", "Gender", "Contact", "Symptoms", "Duration", "Medications", "Follow-up"):
        tree.column(col, width=100, anchor="center")
    
    # Insert data into the Treeview
    for record in records:
        tree.insert("", "end", values=record)
    
    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    # Pack the Treeview and scrollbar in the window
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Initialize the main window
root = tk.Tk()
root.title("Healthcare Form")
root.geometry("550x650")
root.configure(bg="#f2f2f2")  # Light background color

# Header
header_frame = tk.Frame(root, bg="#4CAF50")
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="Healthcare Form", font=("Helvetica", 18), bg="#4CAF50", fg="white").pack(pady=10)

# Content Frame
content_frame = tk.Frame(root, bg="#f2f2f2")
content_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Define and create input fields with labels and voice buttons
def create_labeled_entry(label_text, entry_var, question):
    frame = tk.Frame(content_frame, bg="#f2f2f2")
    frame.pack(fill=tk.X, pady=5)

    tk.Label(frame, text=label_text, font=("Arial", 10, "bold"), bg="#f2f2f2").pack(anchor="w")
    entry = tk.Entry(frame, textvariable=entry_var, font=("Arial", 10))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(frame, text="🎤", font=("Arial", 8), command=lambda: fill_field(entry, question)).pack(side=tk.RIGHT, padx=5)
    return entry

# Input Fields
name_entry = create_labeled_entry("Patient's Name", tk.StringVar(), "What is the patient's name?")
age_entry = create_labeled_entry("Patient's Age", tk.StringVar(), "What is the patient's age?")
gender_entry = create_labeled_entry("Gender", tk.StringVar(), "What is the patient's gender?")
contact_entry = create_labeled_entry("Contact Number", tk.StringVar(), "What is the patient's contact number?")
symptoms_entry = create_labeled_entry("Symptoms", tk.StringVar(), "What symptoms does the patient have?")
duration_entry = create_labeled_entry("Duration", tk.StringVar(), "How long has the patient had these symptoms?")
medication_entry = create_labeled_entry("Medications", tk.StringVar(), "Is the patient taking any medications?")
follow_up_entry = create_labeled_entry("Follow-up Appointment", tk.StringVar(), "When is the follow-up appointment?")

# Button Frame
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=20)

# Display Summary, Clear, and View Records Buttons
tk.Button(button_frame, text="Show Summary and Save", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=display_summary).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Clear", font=("Arial", 10, "bold"), bg="#f44336", fg="white", command=clear_fields).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="View Records", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", command=view_database).pack(side=tk.LEFT, padx=10)

# Run the GUI application
root.mainloop()
