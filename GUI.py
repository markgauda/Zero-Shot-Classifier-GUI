
import PySimpleGUI as sg
import multiprocessing
import time
import gc
def loading_thread(terminate_event):
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

def load_animaton(terminate_event):
    loading_layout = [[sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-GIF-IMAGE-')]]
    loading_window = sg.Window('Loading...', loading_layout, finalize=True)
    while not terminate_event.is_set():
        loading_window['-GIF-IMAGE-'].update_animation(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)

if __name__ == "__main__":
    terminate_event = multiprocessing.Event()
    p = multiprocessing.Process(target=loading_thread, args=(terminate_event,))
    p.start()
    import numpy as np
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib
    import classifier_class
    matplotlib.use('TkAgg')



    classifier = classifier_class.Classifier()

    # First the window layout in 2 columns

    def delete_figure_agg(figure_agg):
        figure_agg.get_tk_widget().forget()

    def update_figure(canvas, figure):
        figure_on_canvas = FigureCanvasTkAgg(figure, canvas)
        figure_on_canvas.draw()
        figure_on_canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_on_canvas

    def get_figure(window):
        # terminate_event = multiprocessing.Event()
        # p = multiprocessing.Process(target=load_animaton, args=(terminate_event,))
        # p.start()
        window.write_event_value("-LOADING START-", "")
        result = classifier.classify_text(values["-TEXT TO CLASSIFY-"], values["-CLASS LIST-"].split(","), multi_label_arg=values["-MULTIPLE CLASSES-"])
        window.write_event_value("-LOADING END-", "")
        # terminate_event.set()
        return result


    parameter_column = [
        [
            sg.Text("Generation parameters", size=(40, 2),justification= "center", font=(22)),
            
        ],
        [
            sg.Text("What is the text you want to classify"),
            sg.In(size=(25, 1), enable_events=True, key="-TEXT TO CLASSIFY-"),
        ],
        [        
            sg.Text("Give a comma seperated list of your classes"),
            sg.In(size=(25, 1), enable_events=True, key="-CLASS LIST-")
        ],
        [
            sg.Checkbox("Allow Multiple classes", key="-MULTIPLE CLASSES-")
        ],
        [
            sg.Button('Classify!', size=(25,2)) 
        ]
    ]

    # For now will only show the name of the file that was chosen
    canvas_column = [
        [sg.Canvas(key="-CANVAS-", size=(10,10))]
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(parameter_column),
            sg.VSeperator(),
            sg.Column(canvas_column),
        ]
    ]

    window = sg.Window("Text classifier", layout, finalize=True)



    # Setup Canvas
    terminate_event.set()
    # Run the Event Loop
    fig_agg = None
    loading = False
    while True:
        if loading == True:
            sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message=f'Analysing data', title='Loading', keep_on_top=True)

        if not fig_agg:
            fig_agg = update_figure(window["-CANVAS-"].TKCanvas , matplotlib.pyplot.figure(figsize=(10, 10))) 

        event, values = window.read(timeout=100)
        if event == "Classify!":
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



