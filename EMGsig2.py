import numpy as np
import logging
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from scipy.signal import butter, filtfilt

# Initialize logging with different levels
logging.basicConfig(filename='emg_signal_processor.log', level=logging.INFO)

class EMGProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("EMG Signal Processor")
        self.create_widgets()

    def create_widgets(self):
        params = [
            ("Sampling Frequency (Hz)", "1000"),
            ("Signal Frequency (Hz)", "10"),
            ("Noise Level", "0.2"),
            ("Lowcut Frequency (Hz)", "20"),
            ("Highcut Frequency (Hz)", "499"),
            ("Filter Order", "4")
        ]

        for i, (text, default) in enumerate(params):
            Label(self.master, text=text).grid(row=i, column=0)
            entry = Entry(self.master)
            entry.grid(row=i, column=1)
            entry.insert(0, default)
            setattr(self, text.replace(" ", "_").lower() + "_entry", entry)

        self.preset_var = StringVar()
        self.preset_var.set("Custom")
        presets = Combobox(self.master, textvariable=self.preset_var, values=["Custom", "Preset 1", "Preset 2"])
        presets.grid(row=len(params), column=1)
        Label(self.master, text="Pre-set Configurations").grid(row=len(params), column=0)

        Button(self.master, text="Generate and Filter", command=self.process_emg).grid(row=len(params) + 1, columnspan=2)

        self.fig = Figure(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=len(params) + 2, columnspan=2)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()
        self.canvas.get_tk_widget().grid(row=len(params) + 3, columnspan=2)

    def validate_inputs(self):
        try:
            fs = float(self.sampling_frequency_hz_entry.get())
            f = float(self.signal_frequency_hz_entry.get())
            noise_level = float(self.noise_level_entry.get())
            lowcut = float(self.lowcut_frequency_hz_entry.get())
            highcut = float(self.highcut_frequency_hz_entry.get())
            order = int(self.filter_order_entry.get())
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
        t, emg_signal = self.generate_signal(fs, f, noise_level)
        emg_filtered = self.filter_signal(emg_signal, lowcut, highcut, order, fs)
        self.update_plot(t, emg_signal, emg_filtered)
        logging.info("EMG signal processed and plots updated.")

    def generate_signal(self, fs, f, noise_level):
        t = np.arange(0, 1.0, 1.0/fs)
        np.random.seed(0)
        emg_signal = np.sin(2 * np.pi * f * t)
        noise = noise_level * np.random.normal(size=len(t))
        emg_signal += noise
        return t, emg_signal

    def filter_signal(self, emg_signal, lowcut, highcut, order, fs):
        b, a = butter(order, [lowcut, highcut], btype='band', fs=fs)
        emg_filtered = filtfilt(b, a, emg_signal)
        return emg_filtered

    def update_plot(self, t, emg_signal, emg_filtered):
        self.fig.clear()
        ax1 = self.fig.add_subplot(121)
        ax2 = self.fig.add_subplot(122)
        
        ax1.plot(t, emg_signal)
        ax1.set_title('Generated EMG Signal')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)
        
        ax2.plot(t, emg_filtered)
        ax2.set_title('Filtered EMG Signal')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Amplitude')
        ax2.grid(True)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = Tk()
    app = EMGProcessorApp(root)
    root.mainloop()
