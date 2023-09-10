import numpy as np
import logging
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy.signal import butter, filtfilt

# Initialize logging
logging.basicConfig(filename='emg_signal_processor.log', level=logging.INFO)

class EMGProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("EMG Signal Processor")
        
        # Initialize dictionary to store Entry widgets
        self.entries = {}
        
        # Create the UI elements
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for Sampling Frequency
        ttk.Label(self.master, text='Sampling Frequency (Hz)').grid(row=0, column=0)
        self.entries['fs'] = ttk.Entry(self.master)
        self.entries['fs'].grid(row=0, column=1)
        self.entries['fs'].insert(0, '1000')
        
        # Label and Entry for Signal Frequency
        ttk.Label(self.master, text='Signal Frequency (Hz)').grid(row=1, column=0)
        self.entries['f'] = ttk.Entry(self.master)
        self.entries['f'].grid(row=1, column=1)
        self.entries['f'].insert(0, '10')
        
        # Label and Entry for Noise Level
        ttk.Label(self.master, text='Noise Level').grid(row=2, column=0)
        self.entries['noise'] = ttk.Entry(self.master)
        self.entries['noise'].grid(row=2, column=1)
        self.entries['noise'].insert(0, '0.2')
        
        # Label and Entry for Lowcut Frequency
        ttk.Label(self.master, text='Lowcut Frequency (Hz)').grid(row=3, column=0)
        self.entries['lowcut'] = ttk.Entry(self.master)
        self.entries['lowcut'].grid(row=3, column=1)
        self.entries['lowcut'].insert(0, '20')
        
        # Label and Entry for Highcut Frequency
        ttk.Label(self.master, text='Highcut Frequency (Hz)').grid(row=4, column=0)
        self.entries['highcut'] = ttk.Entry(self.master)
        self.entries['highcut'].grid(row=4, column=1)
        self.entries['highcut'].insert(0, '499')
        
        # Label and Entry for Filter Order
        ttk.Label(self.master, text='Filter Order').grid(row=5, column=0)
        self.entries['order'] = ttk.Entry(self.master)
        self.entries['order'].grid(row=5, column=1)
        self.entries['order'].insert(0, '4')
        
        # Generate and Filter Button
        self.generate_button = ttk.Button(self.master, text='Generate and Filter', command=self.process_emg)
        self.generate_button.grid(row=6, columnspan=2)
        
        # Plot Figure and Canvas
        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().grid(row=7, columnspan=2)

        # Adding Navigation Toolbar
        toolbar_frame = Frame(self.master)
        toolbar_frame.grid(row=8, columnspan=2)
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        self.toolbar.pack()

    def validate_inputs(self):
        try:
            fs = float(self.entries['fs'].get())
            f = float(self.entries['f'].get())
            noise_level = float(self.entries['noise'].get())
            lowcut = float(self.entries['lowcut'].get())
            highcut = float(self.entries['highcut'].get())
            order = int(self.entries['order'].get())
            return fs, f, noise_level, lowcut, highcut, order
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers in all fields.")
            return None

    def process_emg(self):
        logging.info("Attempting to generate and filter EMG signal.")
        
        inputs = self.validate_inputs()
        if inputs is None:
            return
        
        fs, f, noise_level, lowcut, highcut, order = inputs
        
        # Generate synthetic EMG signal
        t = np.linspace(0, 1, fs, endpoint=False)
        emg_signal = np.sin(2 * np.pi * f * t) + noise_level * np.random.normal(size=len(t))
        
        # Apply Butterworth filter
        b, a = butter(order, [lowcut, highcut], btype='band', fs=fs)
        emg_filtered = filtfilt(b, a, emg_signal)
        
        # Update the plot
        self.fig.clear()
        ax1 = self.fig.add_subplot(1, 2, 1)
        ax2 = self.fig.add_subplot(1, 2, 2)
        ax1.plot(t, emg_signal)
        ax1.set_title('Original EMG Signal')
        ax2.plot(t, emg_filtered)
        ax2.set_title('Filtered EMG Signal')
        self.canvas.draw()
        
        logging.info("EMG signal processed and plots updated.")

if __name__ == "__main__":
    root = Tk()
    app = EMGProcessorApp(root)
    root.mainloop()
