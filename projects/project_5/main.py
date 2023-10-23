import tkinter as tk
import time
import requests
from tkinter import font as tkFont

LIGHT_GREEN = "#96E6B3"
FERN_GREEN = "#568259"
TEA_GREEN = "#CCFCCB"
MINT_GREEN = "#F1FFFA"
FONT_NAME = "Courier"

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        # Set the window size
        window_width = 1200  # Adjust the width as needed
        window_height = 600  # Adjust the height as needed
        self.root.geometry(f"{window_width}x{window_height}")

        self.text_to_type = self.get_random_words()
        self.words = self.text_to_type.split()
        self.lines_displayed = 3  # Number of lines to display at a time
        self.words_per_line = 6  # Words per line
        self.typed_words = []

        # Create a custom font with a larger size
        custom_font = tkFont.nametofont("TkDefaultFont")
        custom_font.configure(size=20)  # Adjust the size as needed

        self.label = tk.Label(root, text="Type the following text:", font=(FONT_NAME, 20), background=LIGHT_GREEN)
        self.label.pack(pady=40)

        # formatted_text = "\n".join(" ".join(self.words[i:i + 6]) for i in range(0, 18, 6))
        self.sample_text = tk.Text(root, font=(FONT_NAME, 25), background=LIGHT_GREEN, wrap="word", width=50, height=3, highlightthickness=0)
        self.sample_text.insert("1.0", self.get_initial_lines())
        self.sample_text.config(state='disabled')
        self.sample_text.tag_add('text', '1.0', 'end')
        self.sample_text.tag_configure('text', justify='center')
        self.sample_text.pack(pady=20, padx=20)

        self.input_text = tk.Text(root, font=(FONT_NAME, 25), background=MINT_GREEN, wrap="word", width=50, height=2)
        self.input_text.pack(pady=30)

        self.result_label = tk.Label(root, text="", font=(FONT_NAME, 20), background=LIGHT_GREEN)
        self.result_label.pack(pady=10, padx=20)

        self.error_label = tk.Label(root, text="", font=(FONT_NAME, 20), background=LIGHT_GREEN)
        self.error_label.pack(pady=10)

        self.restart_button = tk.Button(root, text="Restart", font=(FONT_NAME, 20), command=self.restart_game)
        self.restart_button.pack_forget()

        self.timer_label = tk.Label(root, text="Time Left: 60 seconds", font=(FONT_NAME, 20), background=LIGHT_GREEN)
        self.timer_label.place(x=10, y=10)

        self.started_typing = False
        self.current_line = 0
        self.current_char = 0
        self.current_word = 1

        self.input_text.bind("<Key>", self.on_key_press)

    def get_initial_lines(self):
        # Get the initial lines to display
        lines = self.words[:self.lines_displayed * self.words_per_line]
        displayed_text = "\n".join(
            " ".join(lines[i:i + self.words_per_line]) for i in range(0, len(lines), self.words_per_line))
        return displayed_text

    def get_random_words(self):
        url = "https://random-word-api.vercel.app/api?words=250"
        response = requests.get(url)
        if response.status_code == 200:
            words = response.json()
            # print(words)
            return " ".join(words)
        else:
            return "Failed to fetch words."

    def update_sample_text(self):
        start = self.current_line * self.words_per_line
        end = start + (self.lines_displayed * self.words_per_line)
        lines = self.words[start:end]

        formatted_text = "\n".join(" ".join(lines[i:i + self.words_per_line]) for i in range(0, len(lines), self.words_per_line))

        self.sample_text.config(state='normal')
        self.sample_text.delete('1.0', tk.END)
        self.sample_text.insert('1.0', formatted_text)
        self.sample_text.config(state='disabled')
        self.sample_text.tag_add('text', '1.0', 'end')
        self.sample_text.tag_configure('text', justify='center')

    def highlight_current_word(self):
        self.sample_text.tag_remove('highlight', '1.0', '2.0')
        start = self.current_char
        end = start + len(self.words[self.current_word - 1])
        # print(start)
        # print(end)
        self.sample_text.tag_add('highlight', f'1.{start}', f'1.{end}')
        self.sample_text.tag_config('highlight', background=FERN_GREEN, foreground=MINT_GREEN)
        self.current_char = end + 1

    def on_key_press(self, event):
        if not self.started_typing:
            self.start_test()
            self.started_typing = True

    def start_test(self):
        if not hasattr(self, "start_time"):
            self.start_time = time.time()
            self.end_time = self.start_time + 60  # Limit test to 60 seconds

        self.input_text.config(state="normal")
        self.input_text.bind("<KeyRelease>", self.check_text)
        self.root.after(1000, self.update_timer)

    def update_timer(self):
        current_time = time.time()
        time_left = max(0, self.end_time - current_time)
        self.timer_label.config(text=f"Time Left: {int(time_left)} seconds")

        if time_left <= 0:
            self.input_text.unbind("<KeyRelease>")
            typed_text = self.input_text.get("1.0", tk.END)
            typed_words = typed_text.split()
            word_count = len(typed_words)

            wrong_words = [(typed_words[i], self.words[i]) for i in range(len(typed_words)) if
                           i >= len(self.words) or typed_words[i] != self.words[i]
                           ]

            original_wpm = int(word_count / 1)
            wpm = original_wpm - len(wrong_words)
            result_text = f"Words Typed: {wpm} WPM\n\n"

            if len(wrong_words) == 0:
                info_text = "You made no mistakes! Great job!\n\n"
            else:
                info_text = (
                    f"In reality, you typed {original_wpm} WPM, but you made {len(wrong_words)} mistakes, which were not counted in your WPM score.\n\n"
                )

            self.result_label.config(text=result_text + info_text)

            self.restart_button.pack(pady=10)

            if wrong_words:
                error_text = "Your mistakes were:\n"
                for wrong_word, correct_word in wrong_words:
                    error_text += f'Instead of "{correct_word}", you typed "{wrong_word}"\n'
                self.error_label.config(text=error_text)
        else:
            self.root.after(1000, self.update_timer)

    def check_text(self, event):
        typed_text = self.input_text.get("1.0", tk.END)
        typed_words = typed_text.split()

        self.typed_words = typed_words

        if typed_text == self.text_to_type:
            self.input_text.unbind("<KeyRelease>")

        if len(self.typed_words) > (self.current_line * self.words_per_line) + self.words_per_line:
            self.current_line += 1
            self.current_char = 0
            self.update_sample_text()

        if len(self.typed_words) == self.current_word:
            self.highlight_current_word()
            self.current_word += 1

    def restart_game(self):
        self.restart_button.pack_forget()

        # Close the current window and destroy it
        self.root.destroy()

        # Create a new Tkinter window
        root = tk.Tk()
        root.configure(bg="#96E6B3")  # Change the background color of the root window

        # Recreate the TypingSpeedApp object
        app = TypingSpeedApp(root)

        # Start the main loop for the new window
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#96E6B3")  # Change the background color of the root window

    app = TypingSpeedApp(root)
    root.mainloop()