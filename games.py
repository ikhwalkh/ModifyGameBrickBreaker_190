import tkinter as tk
import random

class BrickBreaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Brick Breaker Game")
        self.root.resizable(False, False)

        self.width = 800
        self.height = 600

        self.canvas = tk.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#17172b"
        )
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.running = False

        self.paddle = self.canvas.create_rectangle(
            350, 540, 450, 555,
            fill="#ffc800",
            outline=""
        )

        self.ball = self.canvas.create_oval(
            390, 510, 410, 530,
            fill="white",
            outline=""
        )

        self.ball_dx = 4
        self.ball_dy = -4

        
        self.info = self.canvas.create_text(
            400, 20,
            text="Score: 0     Lives: 3",
            fill="white",
            font=("Arial", 16, "bold")
        )

        self.bricks = []
        self.create_bricks()

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.start_game)

        
        self.message = self.canvas.create_text(
            400, 300,
            text="PRESS SPACE TO START",
            fill="yellow",
            font=("Arial", 22, "bold")
        )

    def create_bricks(self):
        colors = [
            "#f347ff",
            "#12064f",
            "#00ff6a",
            "#000000"
        ]

        for row in range(4):
            for col in range(10):
                x1 = 30 + col * 75
                y1 = 60 + row * 35
                x2 = x1 + 65
                y2 = y1 + 25

                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=colors[row],
                    outline="white"
                )

                self.bricks.append(brick)

    def move_left(self, event):
        if not self.running:
            return

        x1, y1, x2, y2 = self.canvas.coords(
            self.paddle
        )

        if x1 > 0:
            self.canvas.move(self.paddle, -25, 0)

    def move_right(self, event):
        if not self.running:
            return

        x1, y1, x2, y2 = self.canvas.coords(
            self.paddle
        )

        if x2 < self.width:
            self.canvas.move(self.paddle, 25, 0)

    def start_game(self, event=None):
        if self.running:
            return

        if self.lives <= 0 or len(self.bricks) == 0:
            self.restart_game()
            return

        self.running = True
        self.canvas.delete(self.message)
        self.game_loop()

    def game_loop(self):
        if not self.running:
            return

        self.canvas.move(
            self.ball,
            self.ball_dx,
            self.ball_dy
        )

        x1, y1, x2, y2 = self.canvas.coords(
            self.ball
        )

        
        if x1 <= 0 or x2 >= self.width:
            self.ball_dx *= -1

        
        if y1 <= 0:
            self.ball_dy *= -1

        
        px1, py1, px2, py2 = self.canvas.coords(
            self.paddle
        )

        if (
            y2 >= py1 and
            y1 <= py2 and
            x2 >= px1 and
            x1 <= px2 and
            self.ball_dy > 0
        ):
            self.ball_dy *= -1

        
        overlapping = self.canvas.find_overlapping(
            x1, y1, x2, y2
        )

        for brick in self.bricks[:]:
            if brick in overlapping:
                self.canvas.delete(brick)
                self.bricks.remove(brick)

                self.ball_dy *= -1
                self.score += 10
                self.update_info()
                break

        
        if len(self.bricks) == 0:
            self.end_game("YOU WIN!")
            return

    
        if y2 >= self.height:
            self.lives -= 1
            self.update_info()

            if self.lives <= 0:
                self.end_game("GAME OVER!")
                return

            self.reset_ball()
            return

        self.root.after(16, self.game_loop)

    def reset_ball(self):
        self.running = False

        self.canvas.coords(
            self.ball,
            390, 510, 410, 530
        )

        self.ball_dx = random.choice([-4, 4])
        self.ball_dy = -4

        self.message = self.canvas.create_text(
            400, 300,
            text="PRESS SPACE TO CONTINUE",
            fill="yellow",
            font=("Arial", 20, "bold")
        )

    def update_info(self):
        self.canvas.itemconfig(
            self.info,
            text=f"Score: {self.score}     Lives: {self.lives}"
        )

    def end_game(self, message):
        self.running = False

        self.canvas.create_text(
            400, 300,
            text=message,
            fill="yellow",
            font=("Arial", 30, "bold")
        )

        self.canvas.create_text(
            400, 350,
            text="PRESS SPACE TO RESTART",
            fill="white",
            font=("Arial", 15)
        )

    def restart_game(self):
        self.canvas.delete("all")

        self.score = 0
        self.lives = 3
        self.running = False

        self.paddle = self.canvas.create_rectangle(
            350, 540, 450, 555,
            fill="#00d4ff",
            outline=""
        )

        self.ball = self.canvas.create_oval(
            390, 510, 410, 530,
            fill="white",
            outline=""
        )

        self.ball_dx = 4
        self.ball_dy = -4

        self.info = self.canvas.create_text(
            400, 20,
            text="Score: 0     Lives: 3",
            fill="white",
            font=("Arial", 16, "bold")
        )

        self.bricks = []
        self.create_bricks()

        self.message = self.canvas.create_text(
            400, 300,
            text="PRESS SPACE TO START",
            fill="yellow",
            font=("Arial", 22, "bold")
        )



if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreaker(root)
    root.mainloop()
