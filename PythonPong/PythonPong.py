from tkinter import *
import random

#deze gebruiken voor hindernissen
#        if self.collissionObject.count(3) > 0 or self.collissionObject.count(4) > 0:
#            print("Bounce player :", canvas.find_overlapping(self.position[0], self.position[1], self.position[2], self.position[3]))
#            self.ballDirection[0] *= -1 
#
#   TODO
#   
#   - bounce uiteinden spelers
#   - reset game 
#   - user input
#   - label position on foreground?
#   * bot begint op eigen helft
#

class Ball:

    def __init__(self, canvas, width, height):
        self.canvasWidth = width
        self.canvasHeight = height
        self.ballRadius = 10
        self.ballVector = [-3, -2, -1, 1, 2, 3]
        self.ballCoor = [self.canvasWidth/2, self.canvasHeight/2]
        self.ballDirection = [self.ballVector[random.randint(0, 5)], self.ballVector[random.randint(0, 5)]]
        self.x0 = self.ballCoor[0] - self.ballRadius
        self.y0 = self.ballCoor[1] - self.ballRadius
        self.x1 = self.ballCoor[0] + self.ballRadius
        self.y1 = self.ballCoor[1] + self.ballRadius      
        self.ball = canvas.create_oval(self.x0, self.y0, self.x1, self.y1, fill="Orange Red")

    def position(self):
        self.ballPosition = canvas.coords(self.ball)
        return self.ballPosition     
    
    def checkCollision(self):  
        self.position = canvas.coords(self.ball)
        self.collissionObject = canvas.find_overlapping(*self.position)
     #   print("Bounce player :", canvas.find_overlapping(*self.position))
        if self.collissionObject.count(3) > 0 or self.collissionObject.count(5) > 0:          
            self.ballDirection[0] *= -1 
        #    print("Bounce player :", canvas.find_overlapping(*self.position))
        if self.position[0] <= 0:
            playerTwo.score += 1
            playerTwo.scoreStringVar.set(str(playerTwo.score))
            self.ballDirection[0] *= -1 
        if self.position[2] >= self.canvasWidth+2:     
            playerOne.score += 1
            playerOne.scoreStringVar.set(str(playerOne.score))
            self.ballDirection[0] *= -1 
       #     print("Bounce X-as   :", self.position)
        if self.position[1] <= 0 or self.position[3] >= self.canvasHeight+2:    # boven onder
       #     print("Bounce Y-as   :", self.position)
            self.ballDirection[1] *= -1   

    def moveBall(self):
        canvas.move(self.ball, self.ballDirection[0], self.ballDirection[1]) 


class Player:

    def __init__(self, canvas, width, height, player):
        self.playerHeight = height/5
        self.playerWidth = 5
        self.canvasWidth = width
        self.canvasHeight = height
        self.playerDistance = 50
        self.score = 0
        self.scoreStringVar = StringVar()
        self.scoreStringVar.set(str(self.score))
        self.scoreLabel = Label(canvas, textvariable=self.scoreStringVar, bg="black", fg="grey", font=('Verdana', 18, 'bold'))
        self.scoreLabel.pack()
        if player == 1:
            self.x0 = self.playerDistance
            self.x1 = self.playerDistance 
            self.playerDirectionAI = -2
            canvas.create_window(canvasWidth/2 - canvasWidth/10, canvasHeight/10, window=self.scoreLabel)
        else:
            self.x0 = self.canvasWidth - self.playerDistance
            self.x1 = self.canvasWidth - self.playerDistance
            self.playerDirectionAI = 2
            canvas.create_window(canvasWidth/2 + canvasWidth/10, canvasHeight/10, window=self.scoreLabel)
        self.y0 = (self.canvasHeight/2) - (self.playerHeight/2)
        self.y1 = self.y0 + self.playerHeight
        self.player = canvas.create_line(self.x0, self.y0, self.x1, self.y1, fill="white", width=self.playerWidth)

    def bot(self):
        self.ballPosition = ball.position
        if self.ballPosition[1] >= self.playerHeight/2 and self.ballPosition[3] <= self.canvasHeight-self.playerHeight/2:
            canvas.move(self.player, 0, ball.ballDirection[1])
        
    def move(self):
        self.playerPosition = canvas.coords(self.player)      
        if self.playerPosition[1] <= 10 or self.playerPosition[3] >= self.canvasHeight-10:    # boven onder
            self.playerDirectionAI *= -1
        canvas.move(self.player, 0, self.playerDirectionAI)
 

if __name__ == "__main__":
    canvasWidth = 600
    canvasHeight = 400

    root = Tk()
    root.geometry(str(canvasWidth) + "x" + str(canvasHeight) + "+400+200")
    root.minsize(canvasWidth, canvasHeight)
    root.maxsize(canvasWidth, canvasHeight)
    root.title("Python Pong")

    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, bg="black")
    canvas.pack()

    middleLine = canvas.create_line(canvasWidth/2, 0, canvasWidth/2, canvasHeight, fill="grey", dash=(250, 5))

    playerOne = Player(canvas, canvasWidth, canvasHeight, 1)
    playerTwo = Player(canvas, canvasWidth, canvasHeight, 2)

    ball = Ball(canvas, canvasWidth, canvasHeight)
 
    while True:
        ball.moveBall() 
        ball.checkCollision()
        playerOne.move()
        playerTwo.bot()
        root.update()
        root.after(10)
    
    root.mainloop()