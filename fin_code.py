import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import time
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import queue

conn = sqlite3.connect('shm_data.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS sensor_data (timestamp TEXT, vibration REAL, stress REAL, temperature REAL)')
conn.commit()

model = LinearRegression()
X_train = np.array([[0], [1], [2], [3], [4], [5]])
y_train = np.array([0.5, 1.2, 1.9, 3.1, 3.8, 4.9])
model.fit(X_train, y_train)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('AI-Enabled Structural Health Monitoring')
        self.geometry('1200x700')
        self.chat_queue = queue.Queue()
        self.create_widgets()
        self.update_sensor_data()

    def create_widgets(self):
        self.left_frame = tk.Frame(self, width=300, bg='lightgray')
        self.left_frame.pack(side='left', fill='y')
        self.mid_frame = tk.Frame(self)
        self.mid_frame.pack(side='left', fill='both', expand=True)
        self.right_frame = tk.Frame(self, width=300, bg='white')
        self.right_frame.pack(side='right', fill='y')

        self.sensor_tree = ttk.Treeview(self.left_frame, columns=('vibration', 'stress', 'temp'), show='headings')
        self.sensor_tree.heading('vibration', text='Vibration')
        self.sensor_tree.heading('stress', text='Stress')
        self.sensor_tree.heading('temp', text='Temp')
        self.sensor_tree.pack(fill='both', expand=True, pady=10)

        self.plot_button = tk.Button(self.left_frame, text='Plot Graphs', command=self.plot_graph)
        self.plot_button.pack(pady=5)

        self.ai_label = tk.Label(self.left_frame, text='AI Prediction')
        self.ai_label.pack(pady=5)
        self.ai_entry = tk.Entry(self.left_frame)
        self.ai_entry.pack(pady=5)
        self.ai_result = tk.Label(self.left_frame, text='Result: N/A')
        self.ai_result.pack(pady=5)
        self.ai_button = tk.Button(self.left_frame, text='Predict', command=self.predict_ai)
        self.ai_button.pack(pady=5)

        self.chat_display = tk.Text(self.right_frame, height=30, width=40, state='disabled', bg='#f9f9f9')
        self.chat_display.pack(pady=10)
        self.chat_entry = tk.Entry(self.right_frame)
        self.chat_entry.pack(pady=5)
        self.chat_send = tk.Button(self.right_frame, text='Send', command=self.send_chat)
        self.chat_send.pack()

        self.alert_label = tk.Label(self.right_frame, text='', fg='red', font=('Arial', 12, 'bold'))
        self.alert_label.pack(pady=10)

        self.fig, self.ax = plt.subplots(3, 1, figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.mid_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def update_sensor_data(self):
        vib = round(random.uniform(0.0, 5.0), 2)
        stress = round(random.uniform(0.0, 10.0), 2)
        temp = round(random.uniform(20.0, 60.0), 2)
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute('INSERT INTO sensor_data VALUES (?, ?, ?, ?)', (ts, vib, stress, temp))
        conn.commit()
        self.sensor_tree.insert('', 0, values=(vib, stress, temp))
        self.analyze_data(vib, stress, temp)
        self.after(3000, self.update_sensor_data)

    def analyze_data(self, vib, stress, temp):
        if vib > 4.0 or stress > 8.0 or temp > 50.0:
            self.alert_label.config(text='Structural Alert Triggered!')
        else:
            self.alert_label.config(text='')

    def plot_graph(self):
        cur.execute('SELECT * FROM sensor_data ORDER BY ROWID DESC LIMIT 20')
        data = cur.fetchall()[::-1]
        timestamps = [d[0][-8:] for d in data]
        vibrations = [d[1] for d in data]
        stresses = [d[2] for d in data]
        temps = [d[3] for d in data]
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()
        self.ax[0].plot(timestamps, vibrations, label='Vibration', color='blue')
        self.ax[1].plot(timestamps, stresses, label='Stress', color='green')
        self.ax[2].plot(timestamps, temps, label='Temperature', color='red')
        self.ax[0].legend()
        self.ax[1].legend()
        self.ax[2].legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def predict_ai(self):
        try:
            val = float(self.ai_entry.get())
            pred = model.predict(np.array([[val]]))[0]
            self.ai_result.config(text=f'Result: {round(pred, 2)}')
        except:
            self.ai_result.config(text='Result: Invalid input')

    def send_chat(self):
        user_input = self.chat_entry.get().strip()
        if user_input:
            self.display_chat('You', user_input)
            Thread(target=self.chat_response, args=(user_input,)).start()
            self.chat_entry.delete(0, 'end')

    def chat_response(self, msg):
        time.sleep(1)
        if 'stress' in msg.lower():
            response = 'Structural stress above 8.0 may indicate critical failure.'
        elif 'temperature' in msg.lower():
            response = 'High temperature can weaken materials over time.'
        elif 'vibration' in msg.lower():
            response = 'Excessive vibration indicates possible instability.'
        elif 'safe' in msg.lower():
            response = 'Safety is ensured if all readings are within normal thresholds.'
        else:
            response = 'Monitoring data continuously. Please ask about stress, temp, or vibration.'
        self.display_chat('Bot', response)

    def display_chat(self, sender, msg):
        self.chat_display.config(state='normal')
        self.chat_display.insert('end', f'{sender}: {msg}\n')
        self.chat_display.config(state='disabled')
        self.chat_display.yview('end')

app = App()
app.mainloop()