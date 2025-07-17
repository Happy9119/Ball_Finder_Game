import tkinter as tk
from tkinter import messagebox
import random
import os

try:
    from playsound import playsound
    SOUND_SUPPORT = True
except ImportError:
    SOUND_SUPPORT = False


class FindTheBallUltimate:
    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Find The Ball - ULTIMATE")
        self.master.geometry("800x500")
        self.master.resizable(False, False)

        # Game state
        self.score = {'wins': 0, 'losses': 0}
        self.time_left = 10
        self.difficulty = 'Medium'
        self.highscore = self.load_highscore()

        # GUI Layout
        self.title_label = tk.Label(master, text="🎩 FIND THE BALL - ULTIMATE 🎩", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        self.timer_label = tk.Label(master, text=f"Time Left: {self.time_left}s", font=("Arial", 14))
        self.timer_label.pack()

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=30)

        self.cup_buttons = []
        for i in range(4):
            btn = tk.Button(self.buttons_frame, text=f"🎩 Cup {i + 1}", font=("Arial", 16),
                            width=12, height=4, command=lambda i=i: self.make_guess(i))
            btn.grid(row=0, column=i, padx=15)
            self.cup_buttons.append(btn)

        self.status_label = tk.Label(master, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.score_label = tk.Label(master, text=self.get_score_text(), font=("Arial", 14))
        self.score_label.pack()

        self.highscore_label = tk.Label(master, text=f"🏆 Highscore: {self.highscore}", font=("Arial", 14))
        self.highscore_label.pack(pady=5)

        self.controls_frame = tk.Frame(master)
        self.controls_frame.pack(pady=15)

        self.play_again_btn = tk.Button(self.controls_frame, text="Play Again", font=("Arial", 12),
                                        command=self.reset_game, state="disabled")
        self.play_again_btn.grid(row=0, column=0, padx=10)

        self.quit_btn = tk.Button(self.controls_frame, text="Exit", font=("Arial", 12),
                                  command=self.master.quit)
        self.quit_btn.grid(row=0, column=1, padx=10)

        self.difficulty_label = tk.Label(self.controls_frame, text="Difficulty:", font=("Arial", 12))
        self.difficulty_label.grid(row=0, column=2, padx=10)

        self.difficulty_var = tk.StringVar(value=self.difficulty)
        self.difficulty_menu = tk.OptionMenu(self.controls_frame, self.difficulty_var, "Easy", "Medium", "Hard",
                                             command=self.change_difficulty)
        self.difficulty_menu.grid(row=0, column=3, padx=10)

        self.shuffle_cups(animated=True)
        self.start_timer()

    def get_score_text(self):
        return f"Wins: {self.score['wins']} | Losses: {self.score['losses']}"

    def load_highscore(self):
        if os.path.exists("highscore.txt"):
            try:
                with open("highscore.txt", "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def save_highscore(self):
        if self.score['wins'] > self.highscore:
            with open("highscore.txt", "w") as f:
                f.write(str(self.score['wins']))
            self.highscore = self.score['wins']
            self.highscore_label.config(text=f"🏆 Highscore: {self.highscore}")

    def shuffle_cups(self, animated=False):
        self.cups = ['', '', '', 'O']
        random.shuffle(self.cups)
        self.status_label.config(text="")
        self.time_left = self.get_time_limit()
        self.timer_label.config(text=f"Time Left: {self.time_left}s")

        for btn in self.cup_buttons:
            btn.config(state="normal")

        self.play_again_btn.config(state="disabled")

        if animated:
            self.animate_shuffle(10)

    def animate_shuffle(self, times):
        if times > 0:
            random.shuffle(self.cups)
            self.master.after(100, lambda: self.animate_shuffle(times - 1))

    def get_time_limit(self):
        if self.difficulty == 'Easy':
            return 15
        elif self.difficulty == 'Hard':
            return 5
        else:
            return 10

    def make_guess(self, index):
        self.master.after_cancel(self.timer_job)
        if self.cups[index] == 'O':
            self.status_label.config(text="✅ Correct! You found the ball!", fg="green")
            self.score['wins'] += 1
            if SOUND_SUPPORT:
                playsound("success.mp3")
        else:
            correct_index = self.cups.index('O')
            self.status_label.config(
                text=f"❌ Wrong! The ball was under Cup {correct_index + 1}.",
                fg="red"
            )
            self.score['losses'] += 1
            if SOUND_SUPPORT:
                playsound("fail.mp3")

        for btn in self.cup_buttons:
            btn.config(state="disabled")

        self.score_label.config(text=self.get_score_text())
        self.save_highscore()
        self.play_again_btn.config(state="normal")

    def reset_game(self):
        self.shuffle_cups(animated=True)
        self.start_timer()

    def start_timer(self):
        self.timer_job = self.master.after(1000, self.update_timer)

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.config(text=f"Time Left: {self.time_left}s")

        if self.time_left <= 0:
            self.status_label.config(
                text="⏰ Time's up! You missed the guess!",
                fg="orange"
            )
            correct_index = self.cups.index('O')
            self.status_label.config(
                text=f"⏰ Time's up! The ball was under Cup {correct_index + 1}.",
                fg="orange"
            )
            self.score['losses'] += 1
            self.score_label.config(text=self.get_score_text())
            for btn in self.cup_buttons:
                btn.config(state="disabled")
            self.save_highscore()
            self.play_again_btn.config(state="normal")
            if SOUND_SUPPORT:
                playsound("fail.mp3")
        else:
            self.start_timer()

    def change_difficulty(self, choice):
        self.difficulty = choice
        self.reset_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = FindTheBallUltimate(root)
    root.mainloop()
