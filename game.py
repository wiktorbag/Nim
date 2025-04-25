import tkinter as tk
import random

class NimGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nim Game")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        # Strategy selection
        self.strategy_var = tk.StringVar(value="MAJTEK")
        self.strategy_frame = tk.Frame(root)
        self.strategy_frame.pack(pady=5)

        tk.Label(self.strategy_frame, text="Wybeirz strategię komputera:").pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(self.strategy_frame, self.strategy_var, "PIRAT", "MAJTEK").pack(side=tk.LEFT)

        # Game Mode Buttons
        self.mode_frame = tk.Frame(root)
        self.mode_frame.pack(pady=10)

        tk.Label(self.mode_frame, text="Wybierz tryb gry:").pack(side=tk.LEFT, padx=5)
        tk.Button(self.mode_frame, text="Jeden stos", command=self.start_single_heap).pack(side=tk.LEFT, padx=5)
        tk.Button(self.mode_frame, text="Kilka stosów (3–5)", command=self.start_multi_heap).pack(side=tk.LEFT, padx=5)

        # Player Input Section
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Wybierz numer stosu:").pack(side=tk.LEFT)
        self.heap_choice = tk.Entry(self.input_frame, width=5)
        self.heap_choice.pack(side=tk.LEFT, padx=5)

        tk.Label(self.input_frame, text="Ilość elementów do usunięcia:").pack(side=tk.LEFT)
        self.remove_count = tk.Entry(self.input_frame, width=5)
        self.remove_count.pack(side=tk.LEFT, padx=5)

        self.submit_button = tk.Button(self.input_frame, text="Zrób ruch", command=self.submit_move)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(root, text="", fg="red")
        self.status_label.pack(pady=5)

        self.heaps = []
        self.game_over = False

    def start_single_heap(self):
        self.heaps = [random.randint(5, 10)]
        self.game_over = False
        self.draw_heaps()
        self.status_label.config(text="Twoja kolej!")

    def start_multi_heap(self):
        num_heaps = random.randint(3, 5)
        self.heaps = [random.randint(3, 7) for _ in range(num_heaps)]
        self.game_over = False
        self.draw_heaps()
        self.status_label.config(text="Twoja kolej!")

    def draw_heaps(self):
        self.canvas.delete("all")
        heap_width = 80
        spacing = 20
        base_y = 300
        rect_height = 20

        total_width = len(self.heaps) * (heap_width + spacing)
        start_x = (600 - total_width) // 2

        for i, heap_size in enumerate(self.heaps):
            x0 = start_x + i * (heap_width + spacing)

            for j in range(heap_size):
                y0 = base_y - j * (rect_height + 5)
                self.canvas.create_rectangle(
                    x0, y0, x0 + heap_width, y0 + rect_height,
                    fill="skyblue", outline="black"
                )

            self.canvas.create_text(x0 + heap_width // 2, base_y + 30, text=f"stos {i+1}")
            self.canvas.create_text(x0 + heap_width // 2, base_y + 50, text=f"zostało: {heap_size}")

    def submit_move(self):
        if self.game_over:
            return

        try:
            heap_index = int(self.heap_choice.get()) - 1
            count = int(self.remove_count.get())

            if heap_index < 0 or heap_index >= len(self.heaps):
                self.status_label.config(text="Niedopowiedni numer stosu.")
                return

            if count < 1 or count > self.heaps[heap_index]:
                self.status_label.config(text="Nieodpowiednia liczba zabranych elementów.")
                return

            # Player move
            self.heaps[heap_index] -= count
            self.draw_heaps()

            if self.check_game_over("Player"):
                return

            # Computer move
            self.root.after(700, self.computer_move)

        except ValueError:
            self.status_label.config(text="Wpisz odpowiednie liczby.")

    def computer_move(self):
        strategy = self.strategy_var.get()

        if strategy == "MAJTEK":
            self.majtek_move()
        else:
            self.pirat_move()

        self.draw_heaps()
        self.check_game_over("Computer")

    def majtek_move(self):
        non_empty_heaps = [(i, h) for i, h in enumerate(self.heaps) if h > 0]
        if not non_empty_heaps:
            return

        heap_index, heap_size = random.choice(non_empty_heaps)
        remove_count = random.randint(1, heap_size)
        self.heaps[heap_index] -= remove_count

        self.status_label.config(text=f"MAJTEK zabiera {remove_count} ze stosu {heap_index+1}")

    def pirat_move(self):
        nim_sum = 0
        for h in self.heaps:
            nim_sum ^= h

        if nim_sum == 0:
            # Losing position, fallback to MAJTEK
            self.majtek_move()
            self.status_label.config(text="PIRAT w tarapatach! ")
            return

        for i, h in enumerate(self.heaps):
            target = h ^ nim_sum
            if target < h:
                removed = h - target
                self.heaps[i] = target
                self.status_label.config(text=f"PIRAT zabiera {removed} ze stosu {i+1}")
                return

    def check_game_over(self, last_player):
        if all(h == 0 for h in self.heaps):
            self.game_over = True
            if last_player == "Player":
                self.status_label.config(text="Wygrałeś! 🎉")
            else:
                self.status_label.config(text=f"{self.strategy_var.get()} wygrał! 💀")
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = NimGameApp(root)
    root.mainloop()
