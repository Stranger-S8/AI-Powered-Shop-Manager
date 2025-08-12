import tkinter as tk
from tkinter import font

class ResizableTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resizable Text Example")
        
        # Create a Label widget
        self.label = tk.Label(self.root, text="Resizable Text", font=("Arial", 20))
        self.label.pack(padx=20, pady=20)

        # Bind window resizing event
        self.root.bind("<Configure>", self.resize_text)

    def resize_text(self, event):
        # Get the current width of the window
        window_width = event.width

        # Calculate new font size based on the window width
        new_font_size = int(window_width / 10)  # Adjust the divisor for different text sizes

        # Update the label's font size
        self.label.config(font=("Arial", new_font_size))

# Create the main window
root = tk.Tk()
app = ResizableTextApp(root)
root.mainloop()
