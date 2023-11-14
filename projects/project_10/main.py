import os
import tkinter as tk
from tkinter import filedialog, messagebox
from google.cloud import texttospeech
import PyPDF2

# Set the path to your service account key JSON file
key_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize the Text-to-Speech client
client = texttospeech.TextToSpeechClient()


# Function to handle the PDF selection
def select_pdf():
    global pdf_file_path, selected_file_label
    # Open a file dialog to select a PDF file
    pdf_file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    # Update the selected file label if a file is selected
    if pdf_file_path:
        selected_file_label.config(text=f"Selected File: {os.path.basename(pdf_file_path)}")
    else:
        selected_file_label.config(text="Selected File: ")


# Function to convert the selected PDF to audio
def convert_to_audio():
    global pdf_file_path
    if not pdf_file_path:
        print("No PDF file selected. Please select a PDF file first.")
    else:
        # Extract the base name of the PDF file (without the extension)
        pdf_base_name = os.path.splitext(os.path.basename(pdf_file_path))[0]

        # Extract text from the selected PDF
        text = ""
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        # Set the text input for synthesis
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Configure voice parameters
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the audio encoding
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Get the user's home directory
        home_directory = os.path.expanduser("~")

        # Specify a "Downloads" directory within the user's home directory
        downloads_directory = os.path.join(home_directory, "Downloads")

        # Define the full path to the output MP3 file in the Downloads directory
        output_file_path = os.path.join(downloads_directory, f"{pdf_base_name}.mp3")

        # Perform the text-to-speech conversion
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the audio content to the specified file path
        with open(output_file_path, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_file_path}"')

        # Show a success message
        messagebox.showinfo("Success", f"Audio content written to file '{output_file_path}'")
        pdf_file_path = None
        selected_file_label.config(text="Selected File: ")

# Create the main application window
root = tk.Tk()
root.title("PDF to Audiobook Converter")

# Create labels and buttons
label = tk.Label(root, text="Select the PDF you would like to turn into an Audiobook", pady=20, padx=40)
select_button = tk.Button(root, text="Select PDF", command=select_pdf)
convert_button = tk.Button(root, text="Convert", command=convert_to_audio)

# Label to display selected file
selected_file_label = tk.Label(root, text="Selected File: ", padx=40, pady=20)

# Arrange widgets using grid
label.grid(row=0, column=0, columnspan=2)
select_button.grid(row=1, column=0)
convert_button.grid(row=1, column=1)
selected_file_label.grid(row=2, column=0, columnspan=2)

# Initialize the PDF file path variable
pdf_file_path = None

# Start the GUI application
root.mainloop()
