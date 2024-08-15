import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.master.geometry("400x400")
        
        self.board = [[0]*4 for _ in range(4)]
        self.score = 0
        self.high_score = 0
        self.game_over = False
        
        self.undo_board = []
        
        self.create_widgets()
        self.start_game()
    
    def create_widgets(self):
        self.score_label = tk.Label(self.master, text="Score: 0")
        self.score_label.pack()
        
        self.high_score_label = tk.Label(self.master, text="High Score: 0")
        self.high_score_label.pack()
        
        self.undo_button = tk.Button(self.master, text="Undo", command=self.undo_move, state=tk.DISABLED)
        self.undo_button.pack()
        
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()
        
        self.canvas.bind("<Key>", self.key_pressed)
        self.master.bind("<Left>", lambda event: self.move_tiles("left"))
        self.master.bind("<Right>", lambda event: self.move_tiles("right"))
        self.master.bind("<Up>", lambda event: self.move_tiles("up"))
        self.master.bind("<Down>", lambda event: self.move_tiles("down"))
        
        self.master.focus_set()
    
    def start_game(self):
        self.add_new_tile()
        self.add_new_tile()
        self.update_board()
        self.update_score()
        self.update_high_score()
    
    def update_board(self):
        self.canvas.delete("tile")
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                x0, y0 = j * 100, i * 100
                x1, y1 = x0 + 100, y0 + 100
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill=self.get_tile_color(value), tags="tile")
                if value != 0:
                    self.canvas.create_text(x0 + 50, y0 + 50, text=str(value), font=("Arial", 24, "bold"), tags="tile")
        
        self.canvas.update()
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
    
    def update_high_score(self):
        self.high_score_label.config(text=f"High Score: {self.high_score}")
    
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
    
    def move_tiles(self, direction):
        if self.game_over:
            return
        
        self.save_board_state()
        
        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        
        self.add_new_tile()
        self.update_board()
        self.update_score()
        
        if self.is_game_over():
            self.game_over = True
            self.canvas.create_text(200, 200, text="Game Over!", font=("Arial", 24, "bold"), fill="red")
        else:
            self.update_undo_button()
    
    def move_left(self):
        for i in range(4):
            self.board[i] = self.slide_and_merge(self.board[i])
    
    def move_right(self):
        for i in range(4):
            self.board[i] = self.slide_and_merge(self.board[i][::-1])[::-1]
    
    def move_up(self):
        for j in range(4):
            column = [self.board[i][j] for i in range(4)]
            merged_column = self.slide_and_merge(column)
            for i in range(4):
                self.board[i][j] = merged_column[i]
    
    def move_down(self):
        for j in range(4):
            column = [self.board[i][j] for i in range(4)][::-1]
            merged_column = self.slide_and_merge(column)
            for i in range(4):
                self.board[i][j] = merged_column[::-1][i]
    
    def slide_and_merge(self, line):
        result = [0] * 4
        index = 0
        for value in line:
            if value != 0:
                if result[index] == 0:
                    result[index] = value
                elif result[index] == value:
                    result[index] *= 2
                    self.score += result[index]
                    index += 1
                else:
                    index += 1
                    result[index] = value
        return result
    
    def save_board_state(self):
        self.undo_board = [row[:] for row in self.board]
        self.undo_button.config(state=tk.NORMAL)
    
    def undo_move(self):
        self.board = [row[:] for row in self.undo_board]
        self.score = max(0, self.score - 10)  # Penalize score for undo
        self.update_board()
        self.update_score()
        self.update_undo_button()
    
    def update_undo_button(self):
        if not self.undo_board:
            self.undo_button.config(state=tk.DISABLED)
    
    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True
    
    def get_tile_color(self, value):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096: "#3c3a32",
            8192: "#3c3a32", 16384: "#3c3a32", 32768: "#3c3a32", 65536: "#3c3a32",
        }
        return colors.get(value, "#cdc1b4")
    
    def key_pressed(self, event):
        key = event.keysym.lower()
        if key in ["left", "right", "up", "down"]:
            self.move_tiles(key)

def main():
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

if __name__ == "__main__":
    main()
