import tkinter as tk
from tkinter import ttk

from ..context import MLDOGContext
from ..plugin_descriptor import MLDOGApplicationDescription
from ..model.core import Core

from .status_bar import StatusBar
from .data_source_chooser import DataSourceChooser
from .app_chooser import ApplicationChooser
from .wizard import Wizard
from .application import MLDOGApplication



class MLDOGUI(tk.Tk):
    """
    Central UI Application based on tkinter.
    """
    
    def __init__(self, context: MLDOGContext, **kwargs):
        """
        Construct a new UI instance.

        Parameters
        ----------
        context : MLDOGContext
            The application context instance.
        """

        tk.Tk.__init__(self, **kwargs)
        # super().__init__(**kwargs)

        self.context: MLDOGContext = context
        self.core: Core = Core()

        self.ds_wizards: list[Wizard] = [desc.create() for desc in self.context.ds_wizards]

        self.application: MLDOGApplication = None

        self.title(self.context.getName())

        # configure style
        self.style: ttk.Style = ttk.Style(self)
        self.style.layout('Tabless.TNotebook.Tab', []) # new style with tabs turned off
        self.style.configure("Tabless.TNotebook", tabmargins=0, borderwidth = 0, highlightthickness = 0)

        self.style.configure('Heading.TButton', font=(None, 16), padding='50 30')
        self.style.configure('Heading.TLabel', font=(None, 16))
        self.style.configure('Label.TLabel', font=(None, 11))
        self.style.configure('Normal.TLabel', font=(None, 10))
        self.style.configure('Highlight.TLabel', font=(None, 10, 'bold'))
        self.style.configure('Heading.TLabelframe.Label', font=(None, 15))
        self.style.configure('Config.TEntry', font=(None, 10))

        
        # start task observer polling loop
        self.after_idle(lambda: self.triggerTaskObserver())
    

    def run(self):
        """
        Run the UI application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.setup()
        self.mainloop()


    def triggerTaskObserver(self) -> None:
        """
        Method for polling result messages from tasks.

        This method is used to decouple the task processing thread from the ui thread.
        """
        
        # check for new task result messages
        self.core.checkForTaskResults()

        # schedule next trigger in 10ms
        self.after(10, self.triggerTaskObserver)


    def setup(self) -> None:
        """
        Setup UI components.

        This method is called once to create any layout all standard components.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # create menu bar
        self.createMenu()


        # create central frame
        self.mainframe = ttk.Frame(self, padding='12')
        self.mainframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.grid(column=0, row=1, sticky=tk.EW)

        # create status bar
        self.statusbar = StatusBar(self)
        self.statusbar.grid(column=0, row=2, sticky=tk.SW)
        self.statusbar.setDataSource(self.core.getActiveDataSource())

        # create data source and application chooser frames
        self.data_source_chooser = DataSourceChooser(self.mainframe, self.core, self.ds_wizards)
        self.app_chooser = ApplicationChooser(self.mainframe, self, self.context.apps)

        width = 800
        height = 600
        
        x = self.winfo_screenwidth() // 2 - width // 2
        y = self.winfo_screenheight() // 2 - height // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.updateMainFrame()

        # add event listeners
        self.core.addListener('data_source_changed', self.onDataSourceChanged)
        self.core.addListener('task_changed', self.onTaskChanged)

        self.protocol("WM_DELETE_WINDOW", self.shutdown)

    
    def createMenu(self) -> None:
        """
        Helper method for creating the menu bar.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        
        # create menu bar
        self.menubar = tk.Menu(self, tearoff=tk.OFF)
        self['menu'] = self.menubar

        # create menus
        # ---------- data source menu
        self.ds_menu = tk.Menu(self.menubar, tearoff=tk.OFF)
        self.menubar.add_cascade(menu = self.ds_menu, label = 'DataSource')

        # new data source menu
        new_ds_menu = tk.Menu(self.ds_menu, tearoff=tk.OFF)
        self.ds_menu.add_cascade(menu = new_ds_menu, label = 'New...')

        for dsw in self.ds_wizards:
            new_ds_menu.add_command(label = dsw.name, command = lambda wizard = dsw: wizard.show(self, self.core))

        # universal data source controls
        self.ds_menu.add_separator()
        self.ds_menu.add_command(label = 'Start / Stop Measurement', command = self.toggleMeasurement, state=tk.NORMAL if self.core.hasActiveDataSource() and self.core.hasActiveTask() else tk.DISABLED)

        # clear data source control
        self.ds_menu.add_separator()
        self.ds_menu.add_command(label = 'Clear', command = self.core.setDataSource, state=tk.NORMAL if self.core.hasActiveDataSource() else tk.DISABLED)

            

        # ---------- applications menu
        if len(self.context.apps) > 1:
            self.app_menu = tk.Menu(self.menubar, tearoff=tk.OFF)
            self.menubar.add_cascade(menu = self.app_menu, label = 'Apps')

            for app_desc in self.context.apps:
                self.app_menu.add_command(label = app_desc.getName(), command = lambda desc = app_desc: self.activateApplication(desc))
    

    def activateApplication(self, app_desc: MLDOGApplicationDescription = None) -> None:
        """
        Activate the application of the given application description.

        Parameters
        ----------
        app_desc : MLDOGApplicationDescription
            The application description to activate.

        Returns
        -------
        None
        """

        if self.application is not None:
            # shutdown active application
            self.application.shutdown()
            self.core.setTask()
            self.application = None
        
        if app_desc is not None:
            # create application
            self.application = app_desc.create(self.core, self.mainframe)

        self.updateMainFrame()
    

    def toggleMeasurement(self) -> None:
        """
        Toggle a measurement on the active data source.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.core.hasActiveDataSource():
            if self.core.getActiveDataSource().isMeasuring():
                self.core.getActiveDataSource().stopMeasurement()
            elif self.core.hasActiveTask():
                self.core.getActiveDataSource().startMeasurement(self.core.getActiveTask().getDataQueue())
    

    def clearMainFrame(self) -> None:
        """
        Clear/Remove all components from the central main frame.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        for widgets in self.mainframe.winfo_children():
            # widgets.destroy()
            widgets.pack_forget()
    

    def updateMainFrame(self) -> None:
        """
        Update the main frame component.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # clear active components
        self.clearMainFrame()


        # activate central component and construct new title
        title = self.context.getName()
        if self.application is not None:
            title += ' - ' + self.application.getName()

            # show application frame
            self.application.getUI().pack(expand=True, fill='both')
        elif self.core.hasActiveDataSource():
            # show application chooser
            self.app_chooser.pack(expand=True, fill='both')
        else:
            # show data source chooser
            self.data_source_chooser.pack(expand=True, fill='both')

        # update application title
        self.title(title)


    def onDataSourceChanged(self) -> None:
        """
        Handle the exchange of the active data source.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.core.hasActiveDataSource():
            self.ds_menu.entryconfigure("Start / Stop Measurement", state=tk.NORMAL if self.core.hasActiveTask() else tk.DISABLED)
            self.ds_menu.entryconfigure("Clear", state=tk.NORMAL)
        else:
            self.ds_menu.entryconfigure("Start / Stop Measurement", state=tk.DISABLED)
            self.ds_menu.entryconfigure("Clear", state=tk.DISABLED)
        
        self.statusbar.setDataSource(self.core.getActiveDataSource())

        self.updateMainFrame()


    def onTaskChanged(self) -> None:
        """
        Handle the exchange of the active task.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.ds_menu.entryconfigure("Start / Stop Measurement", state=tk.NORMAL if self.core.hasActiveDataSource() and self.core.hasActiveTask() else tk.DISABLED)
    

    def shutdown(self) -> None:
        """
        Shutdown UI application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.application is not None:
            self.application.shutdown()
        
        self.core.setDataSource()
        self.core.setTask()
        self.destroy()
        self.quit()
