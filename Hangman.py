import random
import tkinter as tk

# List of possible words
word_list = ['apple', 'banana', 'orange', 'strawberry', 'kiwi', 'watermelon', 'grape', 'pineapple']


class WordGuessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("800x600")
        self.master.configure(bg='#F8BBD0')  # Background color
        self.word_list = word_list
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 7
        self.initialize_gui()

    def choose_secret_word(self):
        return random.choice(self.word_list).upper()

    def initialize_gui(self):
        self.word_canvas = tk.Canvas(self.master, width=300, height=300, bg="#C8E6C9")  # Word display canvas color
        self.word_canvas.pack(pady=20)

        self.word_display = tk.Label(self.master, text="_ " * len(self.secret_word), font=("Helvetica", 30), bg='#F8BBD0', fg='#4527A0')  # Text color and font
        self.word_display.pack(pady=(40, 20))

        self.buttons_frame = tk.Frame(self.master, bg='#F8BBD0')
        self.buttons_frame.pack(pady=20)
        self.setup_alphabet_buttons()

        button_bg = "#FF80AB"  # Button background color
        button_fg = "#000000"  # Button text color
        button_font = ("Helvetica", 12, "bold")

        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, width=20, height=2, bg=button_bg, fg=button_fg, font=button_font)
        self.reset_button.pack(pady=(10, 0))

    def setup_alphabet_buttons(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        upper_row = alphabet[:13]
        lower_row = alphabet[13:]

        upper_frame = tk.Frame(self.buttons_frame, bg='#F8BBD0')
        upper_frame.pack()
        lower_frame = tk.Frame(self.buttons_frame, bg='#F8BBD0')
        lower_frame.pack()

        button_bg = "#FF80AB"
        button_fg = "#000000"
        button_font = ("Helvetica", 12, "bold")

        for letter in upper_row:
            button = tk.Button(upper_frame, text=letter, command=lambda l=letter: self.guess_letter(l), width=4, height=2, bg=button_bg, fg=button_fg, font=button_font)
            button.pack(side="left", padx=2, pady=2)

        for letter in lower_row:
            button = tk.Button(lower_frame, text=letter, command=lambda l=letter: self.guess_letter(l), width=4, height=2, bg=button_bg, fg=button_fg, font=button_font)
            button.pack(side="left", padx=2, pady=2)

    def guess_letter(self, letter):
        if letter in self.secret_word and letter not in self.correct_guesses:
            self.correct_guesses.add(letter)
        elif letter not in self.incorrect_guesses:
            self.incorrect_guesses.add(letter)
            self.attempts_left -= 1
            self.update_word_canvas()

        self.update_word_display()
        self.check_game_over()

    def update_word_display(self):
        displayed_word = " ".join([letter if letter in self.correct_guesses else "_" for letter in self.secret_word])
        self.word_display.config(text=displayed_word)

    def update_word_canvas(self):
        self.word_canvas.delete("all")
        stages = [self.draw_head, self.draw_body, self.draw_left_arm, self.draw_right_arm, self.draw_left_leg, self.draw_right_leg, self.draw_face]
        for i in range(len(self.incorrect_guesses)):
            if i < len(stages):
                stages[i]()

    def draw_head(self):
        self.word_canvas.create_oval(125, 50, 185, 110, outline="black")

    def draw_body(self):
        self.word_canvas.create_line(155, 110, 155, 170, fill="black")

    def draw_left_arm(self):
        self.word_canvas.create_line(155, 130, 125, 150, fill="black")

    def draw_right_arm(self):
        self.word_canvas.create_line(155, 130, 185, 150, fill="black")

    def draw_left_leg(self):
        self.word_canvas.create_line(155, 170, 125, 200, fill="black")

    def draw_right_leg(self):
        self.word_canvas.create_line(155, 170, 185, 200, fill="black")

    def draw_face(self):
        self.word_canvas.create_line(140, 70, 150, 80, fill="black")  # Left eye
        self.word_canvas.create_line(160, 70, 170, 80, fill="black")  # Right eye
        self.word_canvas.create_arc(140, 85, 170, 105, start=0, extent=-180, fill="black")  # Sad mouth

    def check_game_over(self):
        if set(self.secret_word).issubset(self.correct_guesses):
            self.game_over_message("Congratulations, you've won!")
        elif self.attempts_left == 0:
            self.game_over_message(f"Game over! The word was: {self.secret_word}")

    def game_over_message(self, message):
        stylish_font = ("Helvetica", 18, "italic")
        button_bg = "#FF80AB"
        button_fg = "#000000"
        button_font = ("Helvetica", 12, "bold")

        self.reset_button.pack_forget()
        self.buttons_frame.pack_forget()
        self.game_over_label = tk.Label(self.master, text=message, font=stylish_font, fg="#D81B60", bg='#F8BBD0')
        self.game_over_label.pack(pady=(10, 20))

        if not hasattr(self, 'restart_button'):
            self.restart_button = tk.Button(self.master, text="Restart Game", command=self.reset_game, width=20, height=2, bg=button_bg, fg=button_fg, font=button_font)
        self.restart_button.pack(pady=(10, 20))

    def reset_game(self):
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 7

        self.word_display.config(text="_ " * len(self.secret_word))
        self.word_canvas.delete("all")

        self.buttons_frame.pack()
        self.reset_button.pack(pady=(10, 0))

        if hasattr(self, 'game_over_label') and self.game_over_label.winfo_exists():
            self.game_over_label.pack_forget()
        if hasattr(self, 'restart_button') and self.restart_button.winfo_exists():
            self.restart_button.pack_forget()

def main():
    root = tk.Tk()
    game = WordGuessGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

