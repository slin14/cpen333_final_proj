# Group#: 32
# Student Names: Joshua Ho, Sophie Lin

"""
    This program implements a variety of the snake 
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue        #the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self, queue, game):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour, 
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self, queue, gui):
        self.queue = queue
        self.gui = gui
        self.queueHandler()
    
    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules 
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self, queue):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """

        self.queue = queue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.  
        # Note that the snake appears to have length N*10 by default - i.e. each increment is length 10     
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.05     #speed of snake updates (sec)
        while self.gameNotOver:
            time.sleep(SPEED)       # delay next loop by interval set by speed
            self.move()             # execute move to update internal members
            self.queue.put({"move":self.snakeCoordinates})  # add the move to UI queue handler with the new data

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        #complete the method implementation below

        self.isGameOver(NewSnakeCoordinates)        # check if the game is over before appending the new head to the list
        self.snakeCoordinates.append(NewSnakeCoordinates)

        currentScore = self.score
        # check for prey consumption - that means new snake coordinates adjusted with SNAKE_ICON_WIDTH is within prey rectangle
        # if we have eaten prey, then we don't have to remove a point at the end of the snake
        # if we have not eaten prey, then we have to remove the last point to keep the snake length constant
        
        preyCoord=gui.canvas.coords(gui.preyIcon)         # returns x1,y1,x2,y2 of the prey rectangle
        preyX = (preyCoord[0]+preyCoord[2])/2             # find center of prey rectangle
        preyY = (preyCoord[1]+preyCoord[3])/2

        # if the snake's width is within the prey box
        if(abs(preyX - NewSnakeCoordinates[0])<=SNAKE_ICON_WIDTH/2+5 and abs(preyY - NewSnakeCoordinates[1])<=SNAKE_ICON_WIDTH/2+5):
            self.createNewPrey()                    # creates the new coordinates and tells the GUI to draw it whenever it can
            self.score = currentScore + 1           # increment internal score
            self.queue.put({"score":currentScore + 1})  # tell the GUI to update the score whenever it can
        else:
            self.snakeCoordinates.pop(0)            # remove the earliest snake coordinate if we didn't eat anything

        
    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        #complete the method implementation below

        # change internal state based on arrow inputs, otherwise don't change 
        # down is +Y, up is -Y
        nextX = lastX
        nextY = lastY
        if(self.direction == "Left"):
            nextX = nextX -10
        elif(self.direction == "Right"):
            nextX = nextX +10
        elif(self.direction == "Up"):
            nextY = nextY -10
        elif(self.direction == "Down"):
            nextY = nextY +10            # DOWN actually does a y++ increment
        return (nextX,nextY)


    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        x, y = snakeCoordinates
        #complete the method implementation below
        if((x,y) in self.snakeCoordinates or x<0 or x>WINDOW_WIDTH or y<0 or y>WINDOW_HEIGHT):
            self.gameNotOver = False            # update internal member
            self.queue.put({"game_over":True})  # send updated data to UI queue 

    def createNewPrey(self) -> None:
        """ 
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). 
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
        THRESHOLD = 15   #sets how close prey can be to borders
        #complete the method implementation below

        
        randX = random.randint(THRESHOLD,WINDOW_WIDTH-THRESHOLD)        # generate random x and y, limit to threshold 
        randY = random.randint(THRESHOLD,WINDOW_HEIGHT-THRESHOLD)
        self.queue.put({"prey":(randX-5,randY-5,randX+5,randY+5)})      # tell GUI to update the screen with new prey 

if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300 
    SNAKE_ICON_WIDTH = 15
    
    BACKGROUND_COLOUR = "gray20"   #you may change this colour if you wish
    ICON_COLOUR = "SeaGreen1"        #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game(gameQueue)        #instantiate the game object

    gui = Gui(gameQueue, game)    #instantiate the game user interface
    
    QueueHandler(gameQueue, gui)  #instantiate our queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()
