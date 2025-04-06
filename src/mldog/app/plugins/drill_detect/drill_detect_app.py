import time
import tkinter as tk
from tkinter import ttk
import os

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from mldog.app.plugins.plot.drill_plot_app import DrillProcedurePlotUI, PlotUI
from mldog.app.plugins.plot.drill_plot_model import DrillPlotModel


from ...model.core import Core
from ...ui.application import MLDOGApplication
from ...tasks.drill_detect_task import DrillDetectTask
import matplotlib.backends.backend_tkagg as tkagg
from PIL import Image


class DrillDetectApplication(MLDOGApplication):
    """
    Drill Detect App. GUI Für das Program
    """

    def __init__(self, core: Core, parent: tk.Frame):
        MLDOGApplication.__init__(self, "Drill Detect", core, parent)
        self.ergebnis = None
        
        
        


        self._pause_processing = False

        # configure grid layout weights
        self._ui.columnconfigure(0, weight=1)
        self._ui.rowconfigure(0, weight=0)
        self._ui.rowconfigure(1, weight=1)
        self._ui.rowconfigure(2, weight=0)

        #self.wm_attributes("-transparentcolor", 'grey')
        


        row = 0
        self.label = ttk.Label(
            self._ui, text="Please stand by", style="TLabel",  font=("Courier", 38), background=None
        )
        # label = ttk.Label(self._ui, text="Example Application: Drill Procedure Plotter", style='Heading.TLabel')
        self.label.grid(column=0, row=row, pady=(20, 5), columnspan=2)

        # plot ui
        row = row + 1

        self.canvas_wrapper = ttk.Frame(self._ui, padding="12")
        #self.canvas_wrapper.grid(column=0, row=row, sticky=tk.NSEW)

        # controls
        # row = row + 1

        file = "src/mldog/app/plugins/drill_detect/jackhammer2.gif"
        info = Image.open(file)
        self.frames = info.n_frames
        
        self.photoimage_objects = []
        for i in range(0,info.n_frames,2):
            obj = tk.PhotoImage(file = file, format = f"gif -index {i}")
            self.photoimage_objects.append(obj)


        self.ax = None
        self.fig = None
        self.canvas = None
        self.fig, self.ax = plt.subplots(dpi=100)
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig, self.canvas_wrapper)
        self.toolbar = tkagg.NavigationToolbar2Tk(self.canvas, self.canvas_wrapper)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)
        self.toolbar.update()


        self.gif_label = tk.Label(self._ui, image="")
        self.gif_label.grid(column=0,row=row,sticky=tk.NSEW)
    
    
        self.animation(current_frame = 0)
        model_path = os.path.join(
            "src", "mldog", "app", "tasks", "Model", "HGB_Model.sav"
        )

        self._core.setTask(
            DrillDetectTask(
                model_path,
            ),
            self.handleTaskResult,
        )

    def animation(self,current_frame=0):
        global loop
        image = self.photoimage_objects[current_frame]

        self.gif_label.configure(image = image)
        current_frame = current_frame + 1

        if current_frame == len(self.photoimage_objects):
            current_frame = 0 # reset the current_frame to 0 when end is reached

        loop = self._ui.after(100, lambda: self.animation(current_frame))


    def handleTaskResult(self, data: object) -> None:
        
        """
        Verarbeitet fertigen Borhvorgang mittels der ML Pipeline

        Parameters
        ----------
        data : object
            Array aus Bohrvorgangsdaten
        """
        if isinstance(data, str):
            self.label.config(text=f"{data}")
            if data == "Bohrvorgang gestartet":     
                #self._ui.after(50,lambda: self.animation(0))
                self.canvas_wrapper.grid_remove()
                time.sleep(0.3)
                self.gif_label.grid(column=0,row=1,sticky=tk.NSEW)
            else:
                #self._ui.after_cancel(loop)
                self.gif_label.grid_remove()
                #time.sleep(0.3)
                self.canvas_wrapper.grid(column=0,row=1,sticky=tk.NSEW)
            print(f"received result: {data}")
            
        else:
            self.ax.clear()
            df = data         
            xVals = np.arange(len(df))
            line, = self.ax.plot(xVals, df["Voltage"])
            line, = self.ax.plot(xVals, df["Current"])
            line, = self.ax.plot(xVals, df["# Audio"])
            self.ax.set_xlabel('Zeitschritt [#]')
            self.ax.set_ylabel('Wert')
            self.ax.legend(['Spannung [V]', 'Strom [A]', 'Ton [-]'])
            self.ax.grid()
            self.fig.tight_layout()
            self.canvas.draw()
            