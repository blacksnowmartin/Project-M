# YouTube Video Links GUI

import tkinter as tk
import webbrowser

# Function to open YouTube video
def open_video(url):
    webbrowser.open(url)

# Create main window
root = tk.Tk()
root.title("YouTube Video Links")

# Video data
videos = {
    "Python Programming Tutorial": "https://www.youtube.com/watch?v=rfscVS0vtbw",
    "Data Science with Python": "https://www.youtube.com/watch?v=LHc8j8g1g0A",
    "Machine Learning Basics": "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
}

# Create and place labels and buttons
for video_title, video_url in videos.items():
    frame = tk.Frame(root)
    frame.pack(pady=10)

    label = tk.Label(frame, text=video_title)
    label.pack(side=tk.LEFT)

    button = tk.Button(frame, text="Watch", command=lambda url=video_url: open_video(url))
    button.pack(side=tk.LEFT)

# Run the application
root.mainloop()
