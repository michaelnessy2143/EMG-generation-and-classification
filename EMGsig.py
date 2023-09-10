import numpy as np
from tkinter import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt

# Function to generate, filter, and classify EMG signals
def process_emg():
    # Retrieve values from the text boxes
    fs = float(fs_entry.get())
    f = float(f_entry.get())
    noise_level = float(noise_level_entry.get())
    lowcut = float(lowcut_entry.get())
    highcut = float(highcut_entry.get())
    order = int(order_entry.get())

    # Generate synthetic EMG signal
    t = np.arange(0, 1.0, 1.0/fs)
    np.random.seed(0)  # for reproducibility
    emg_signal = np.sin(2 * np.pi * f * t)
    noise = noise_level * np.random.normal(size=len(t))
    emg_signal += noise

    # Butterworth bandpass filter design
    b, a = butter(order, [lowcut, highcut], btype='band', fs=fs)

    # Apply the filter
    emg_filtered = filtfilt(b, a, emg_signal)

    # Plotting the generated and filtered EMG signals
    fig.clear()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

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

    canvas.draw()

# Create the main window
root = Tk()
root.title("EMG Signal Processor")

# Add text boxes for input parameters
Label(root, text="Sampling Frequency (Hz)").grid(row=0, column=0)
fs_entry = Entry(root)
fs_entry.grid(row=0, column=1)
fs_entry.insert(0, "1000")

Label(root, text="Signal Frequency (Hz)").grid(row=1, column=0)
f_entry = Entry(root)
f_entry.grid(row=1, column=1)
f_entry.insert(0, "10")

Label(root, text="Noise Level").grid(row=2, column=0)
noise_level_entry = Entry(root)
noise_level_entry.grid(row=2, column=1)
noise_level_entry.insert(0, "0.2")

Label(root, text="Lowcut Frequency (Hz)").grid(row=3, column=0)
lowcut_entry = Entry(root)
lowcut_entry.grid(row=3, column=1)
lowcut_entry.insert(0, "20")

Label(root, text="Highcut Frequency (Hz)").grid(row=4, column=0)
highcut_entry = Entry(root)
highcut_entry.grid(row=4, column=1)
highcut_entry.insert(0, "499")

Label(root, text="Filter Order").grid(row=5, column=0)
order_entry = Entry(root)
order_entry.grid(row=5, column=1)
order_entry.insert(0, "4")

# Add button to generate and filter EMG signal
Button(root, text="Generate and Filter", command=process_emg).grid(row=6, columnspan=2)

# Add plots to display generated and filtered EMG signals
fig = Figure(figsize=(10, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=7, columnspan=2)

# Run the Tkinter event loop
root.mainloop()
