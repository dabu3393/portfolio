import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def open_images():
    # Clear the selected photo and thumbnail
    selected_file_path_var.set("")
    selected_thumbnail_var.set("")

    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if file_paths:
        x, y = 0, 0  # Initial coordinates for placing thumbnails
        thumbnail_height = 150  # Set the fixed thumbnail height
        canvas_width = canvas.winfo_width()  # Get the canvas width

        for file_path in file_paths:
            image = Image.open(file_path)
            image.thumbnail((thumbnail_height, thumbnail_height))  # Resize to a thumbnail size
            thumbnail = ImageTk.PhotoImage(image)
            images.append((file_path, thumbnail))

            # Create a label to display the thumbnail with padding and fixed height
            thumbnail_label = tk.Label(
                canvas, image=thumbnail, relief=tk.SOLID, bd=2,
                height=thumbnail_height, width=thumbnail_height
            )
            thumbnail_label.image = thumbnail
            canvas.create_window(x, y, anchor="nw", window=thumbnail_label)
            thumbnail_label.bind("<Button-1>", lambda event, t=thumbnail, p=file_path: select_thumbnail(t, p))

            # Update the coordinates for the next thumbnail
            x += thumbnail_height + 20

            # Check if a new row is needed
            if x >= canvas_width:
                x = 0
                y += thumbnail_height + 20  # 20 is the vertical padding between rows


#  Function to select a thumbnail
def select_thumbnail(thumbnail, file_path):
    selected_file_path_var.set(file_path)  # Store the file path
    selected_thumbnail_var.set(thumbnail)  # Store the ImageTk.PhotoImage object


# Function to add the watermark to the selected image
def add_watermark():
    selected_file_path = selected_file_path_var.get()
    if not selected_file_path:
        result_label.config(text="Please select a thumbnail first.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".jpg")

    try:
        image = Image.open(selected_file_path)
        watermark = Image.open("./img/watermark.png")  # Provide the path to your watermark image

        # Calculate the scaling factor to fill the longest side
        width, height = image.size
        if width > height:
            scale_factor = width / watermark.width
        else:
            scale_factor = height / watermark.height
        new_width = int(watermark.width * scale_factor)
        new_height = int(watermark.height * scale_factor)
        watermark = watermark.resize((new_width, new_height))

        # Set the opacity (transparency) of the watermark
        alpha = 128  # Adjust the alpha value (0-255) for transparency
        watermark.putalpha(alpha)

        # Position the watermark at the bottom right corner
        x = width - watermark.width
        y = height - watermark.height

        image.paste(watermark, (x, y), watermark)
        image.save(output_path)
        result_label.config(text=f"Watermark added and saved to {output_path}")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")


# Create the main application window
app = tk.Tk()
app.title("Image Watermark Adder")

# Set the window size on launch
app.geometry(f"{app.winfo_screenwidth()}x600")

# Set the background color to white for the entire application
app.configure(bg="white")

# Create and configure widgets
open_images_button = tk.Button(app, text="Add Images", command=open_images, highlightbackground="white")
open_images_button.grid(row=0, column=3, sticky="e", pady=10, padx=10)

add_button = tk.Button(app, text="Add Watermark", command=add_watermark, highlightbackground="white")
add_button.grid(row=0, column=2, pady=10)

# Create a scrollable canvas to display thumbnails with a white background
canvas = tk.Canvas(app, bg="white")
canvas.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

# Create a Label to display the selected thumbnail
selected_thumbnail_var = tk.StringVar()
selected_file_path_var = tk.StringVar()  # Variable to store the selected file path
selected_thumbnail_label = tk.Label(app, text="Selected Thumbnail:", bg="white")
selected_thumbnail_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)
selected_thumbnail_info_label = tk.Label(app, textvariable=selected_thumbnail_var, bg="white")
selected_thumbnail_info_label.grid(row=0, column=1, sticky="w", pady=10)

result_label = tk.Label(app, text="", bg="white")
result_label.grid(row=4, column=0, columnspan=4, pady=10)

# List to store selected images and their thumbnails
images = []

app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(1, weight=1)

app.mainloop()
