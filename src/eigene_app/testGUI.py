import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
# Diese Datei erstmals ignorrieren


class DrillGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Test")
        self.root.geometry("1500x1000")

        self.hauptframe = tk.Frame(self.root, width=600, height=500) #Unser menü wovon wir die Messung starten und dann wird uns ein plot angezeigt mit dem ergebnis
        # ist jedoch erstmals nur eine test für die funktionalität welches anschließend ergänzt wird
        self.hauptframe.pack(padx=10, pady=10)
        self.label = tk.Label(self.hauptframe, text="drück auf ok", font=("Arial", 16))
        self.label.pack(pady=50)

        self.ok = tk.Button(self.hauptframe, text="OK", font=("Arial", 16), command=self.plotten) # nachdem auf ok gedrückt wird soll unser hauptframe verschwinden und es soll eine aktuelle messung
        # welches live aufgezeichnet wurde angezeigt werden
        self.ok.pack()

        
        

    def plotten(self):
        self.hauptframe.pack_forget()
        self.frame = tk.Frame(self.root, width=600, height=500)
        self.frame.pack(padx=10, pady=10)
        fig, ax = plt.subplots(figsize=(60, 50))

        df = pd.read_csv("testdaten.csv", sep=",")
        ax.plot(df.index, df)
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)





root = tk.Tk()
gui = DrillGUI(root)
root.mainloop()