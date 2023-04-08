
import PySimpleGUI as sg
import multiprocessing
import time
import gc

def loading_thread(terminate_event):
    """This creates a seperate process that runs the loading window.
    This is nessisary because the AI model is multiple gig and takes 
    a long time to load. So instead of opening the program and having
    nothing apear, a loading screen will appear for feedback reasons.

    Args:
        terminate_event (multiprocessing.Event): This is the event that
        the primary process will signal to tell this process to end and close
    """
    loading_layout = [[sg.Text('Initializing', size=(40, 15), justification='center', key="-LOADING TEXT-")]]
    loading_window = sg.Window('Loading...', loading_layout, finalize=True)
    loading_window["-LOADING TEXT-"].update("Loading program")
    #sg.popup_non_blocking('This is a popup showing that the GUI is running', grab_anywhere=True)
    while not terminate_event.is_set():
        sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message=f'Loading Classifier', title='Loading', keep_on_top=True)
        time.sleep(0.15)
    
    loading_window.close()
    loading_layout = None
    loading_window = None
    gc.collect()

if __name__ == "__main__":
    # The event that will be used to kill the loading screen
    terminate_event = multiprocessing.Event()
    # Setup the loading screen
    p = multiprocessing.Process(target=loading_thread, args=(terminate_event,))
    p.start()

    # Import large libraries
    import numpy as np
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib
    import classifier_class
    matplotlib.use('TkAgg')

    #load and setup classifier model
    classifier = classifier_class.Classifier()

    def delete_figure_agg(figure):
        """This will clear the figure for the GUI screen

        Args:
            figure (matplotlib.figure): A figure object from matplotlib
        """
        figure.get_tk_widget().forget()

    def update_figure(canvas, figure):
        """This will take in a figure element and add
        it to the given canvas in the window

        Args:
            canvas (pysimplegui.canvas): The canvas to add a figure to
            figure (matplotlib.figure): The figure to add to the canvas

        Returns:
            figure: returns the figure for chaining purposes
        """
        figure_on_canvas = FigureCanvasTkAgg(figure, canvas)
        figure_on_canvas.draw()
        figure_on_canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_on_canvas

    def get_figure(window):
        """Loads the figure from the classifier model. This function is meant to be
        called in a new thread, it will take a while for long prompts

        Args:
            window (pysimplegui.window): The window that events can be sent to

        Returns:
            matplotlib.figure: The figure representing the results of the classifier
        """
        window.write_event_value("-LOADING START-", "")
        result = classifier.classify_text(values["-TEXT TO CLASSIFY-"], values["-CLASS LIST-"].split(","), multi_label_arg=values["-MULTIPLE CLASSES-"])
        window.write_event_value("-LOADING END-", "")
        return result



    parameter_column = [
        [
            # The title
            sg.Text("Generation parameters", size=(40, 2),justification= "center", font=(22)),
        ],
        [
            # The text to classify
            sg.Text("What is the text you want to classify"),
            sg.In(size=(25, 1), enable_events=True, key="-TEXT TO CLASSIFY-"),
        ],
        [   
            # The class list
            sg.Text("Give a comma seperated list of your classes"),
            sg.In(size=(25, 1), enable_events=True, key="-CLASS LIST-")
        ],
        [
            # Option for multiple classes to be possible
            sg.Checkbox("Allow Multiple classes", key="-MULTIPLE CLASSES-")
        ],
        [   
            # Submit button
            sg.Button('Classify!', size=(25,2)) 
        ]
    ]
    canvas_column = [
        # Where the graph will be displaid
        [sg.Canvas(key="-CANVAS-", size=(10,10))]
    ]

    # Setup the full layout
    layout = [
        [
            sg.Column(parameter_column),
            sg.VSeperator(),
            sg.Column(canvas_column)
        ]
    ]
    #Finalize the window
    window = sg.Window("Text classifier", layout, finalize=True)

    # Kill the loading screen
    terminate_event.set()
    # Holds the current figure on screen
    fig_agg = None
    # Determins when to have the loading screen present
    loading = False
    while True:
        # If load is true then display loading popup
        if loading == True:
            sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message=f'Analysing data', title='Loading', keep_on_top=True)
        # If there is not current figure, initlize it with an empty figure
        if not fig_agg:
            fig_agg = update_figure(window["-CANVAS-"].TKCanvas , matplotlib.pyplot.figure(figsize=(10, 10))) 
        # Get window information
        event, values = window.read(timeout=100)
        if event == "Classify!":
            # print statement from pysimplegui cookbook
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
            window.perform_long_operation(lambda:
                                           get_figure(window), "-FIGURE-")
            
        if event == "-FIGURE-":
            if fig_agg:
                delete_figure_agg(fig_agg)
            fig_agg = update_figure(window["-CANVAS-"].TKCanvas , values[event]) 
        if event == "-LOADING START-":
            loading = True
        
        if event == "-LOADING END-":
            sg.PopupAnimated(None)
            loading = False

        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    

    window.close()



