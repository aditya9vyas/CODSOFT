import tkinter as tk
import random

class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("500x550")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.user_score = 0
        self.computer_score = 0
        self.choices = ["Rock", "Paper", "Scissors"]
        self.user_choice = None
        self.computer_choice = None

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Rock Paper Scissors", font=("Segoe UI", 20, "bold"), bg="#1e1e2e", fg="#ffffff").pack(pady=20)

        self.result_label = tk.Label(self.root, text="", font=("Segoe UI", 14), bg="#1e1e2e", fg="#dddddd")
        self.result_label.pack(pady=10)

        self.choice_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.choice_frame.pack(pady=20)

        self.buttons = {}
        button_colors = {
            "Rock": "#ffb703",      # bright yellow-orange
            "Paper": "#219ebc",     # sky blue
            "Scissors": "#8ecae6"   # light blue
        }

        for idx, choice in enumerate(self.choices):
            btn = tk.Button(
                self.choice_frame,
                text=choice,
                font=("Segoe UI", 14, "bold"),
                width=10,
                height=2,
                bg=button_colors[choice],
                fg="#000000",  # Set text color to black
                activebackground="#ffffff",
                command=lambda c=choice: self._play(c)
            )
            btn.grid(row=0, column=idx, padx=10)
            self.buttons[choice] = btn

        self.score_label = tk.Label(self.root, text="", font=("Segoe UI", 14, "bold"), bg="#1e1e2e", fg="#cdd6f4")
        self.score_label.pack(pady=10)

        tk.Button(self.root, text="Reset Game", font=("Segoe UI", 12), bg="#ffb703", fg="#000000",
                  activebackground="#ffe066", command=self._reset_game).pack(pady=20)

        self._update_scoreboard()

    def _play(self, user_choice):
        self.user_choice = user_choice
        self.computer_choice = random.choice(self.choices)

        result = self._determine_winner(self.user_choice, self.computer_choice)

        if result == "tie":
            message = "It's a tie!"
        elif result == "user":
            message = "You win this round!"
            self.user_score += 1
        else:
            message = "Computer wins this round!"
            self.computer_score += 1

        self.result_label.config(
            text=f"You chose {self.user_choice}\nComputer chose {self.computer_choice}\n{message}"
        )
        self._animate_choice(self.user_choice)
        self._update_scoreboard()

    def _determine_winner(self, user, computer):
        win_map = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
        if user == computer:
            return "tie"
        elif win_map[user] == computer:
            return "user"
        else:
            return "computer"

    def _animate_choice(self, choice):
        button = self.buttons[choice]
        original_color = button.cget("bg")
        button.config(bg="#a6e3a1")
        self.root.after(300, lambda: button.config(bg=original_color))

    def _update_scoreboard(self):
        self.score_label.config(
            text=f"Score - You: {self.user_score} | Computer: {self.computer_score}"
        )

    def _reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.result_label.config(text="")
        self._update_scoreboard()

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()