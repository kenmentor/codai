import tkinter as tk
import random

# Setting up the main game window
class CatchBallGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Ball Game")
        self.width = 400
        self.height = 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="lightblue")
        self.canvas.pack()

        # Basket (player controlled object)
        self.basket_width = 80
        self.basket = self.canvas.create_rectangle(self.width // 2 - self.basket_width // 2, self.height - 20,
                                                  self.width // 2 + self.basket_width // 2, self.height, fill="blue")

        # Ball variables
        self.balls = []
        self.ball_speed = 8

        # Game variables
        self.score = 0
        self.lives = 3

        # Text for score and lives
        self.score_text = self.canvas.create_text(50, 10, text=f"Score: {self.score}", font=('Arial', 12), fill='black')
        self.lives_text = self.canvas.create_text(350, 10, text=f"Lives: {self.lives}", font=('Arial', 12), fill='black')

        # Bind keys
        root.bind('<Left>', self.move_left)
        root.bind('<Right>', self.move_right)

        # Start the game
        self.update_game()

    def move_left(self, event):
        self.canvas.move(self.basket, -20, 0)
        if self.canvas.coords(self.basket)[0] < 0:
            self.canvas.move(self.basket, 20, 0)

    def move_right(self, event):
        self.canvas.move(self.basket, 20, 0)
        if self.canvas.coords(self.basket)[2] > self.width:
            self.canvas.move(self.basket, -20, 0)

    def create_ball(self):
        x = random.randint(10, self.width - 10)
        ball = self.canvas.create_oval(x - 10, 0, x + 10, 20, fill='red')
        self.balls.append(ball)

    def update_game(self):
        for ball in self.balls:
            self.canvas.move(ball, 0, self.ball_speed)
            if self.canvas.coords(ball)[3] >= self.height:
                if self.check_catch(ball):
                    self.score += 1
                    self.canvas.delete(ball)
                    self.balls.remove(ball)
                else:
                    self.lives -= 1
                    self.canvas.delete(ball)
                    self.balls.remove(ball)

        self.update_texts()

        if self.lives > 0:
            if random.randint(1, 20) == 1:  # Randomly create a new ball
                self.create_ball()
            self.root.after(50, self.update_game)
        else:
            self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over", font=('Arial', 24), fill='red')

    def check_catch(self, ball):
        ball_coords = self.canvas.coords(ball)
        basket_coords = self.canvas.coords(self.basket)
        if basket_coords[0] < ball_coords[0] < basket_coords[2] and basket_coords[1] < ball_coords[3] < basket_coords[3]:
            return True
        return False

    def update_texts(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")


if __name__ == '__main__':
    root = tk.Tk()
    game = CatchBallGame(root)
    root.mainloop()
