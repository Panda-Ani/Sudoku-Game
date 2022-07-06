import pygame
import requests
import time

# intialise the game
pygame.init()

# create the screen
WIDTH = 550
Background_color = (222, 196, 124)
Fixed_color = (33, 25, 82)
new_color = (10, 69, 23)
screen = pygame.display.set_mode((600, 600))


# API for populating the grid
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()["board"]
original_grid = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]


# Title and icon
pygame.display.set_caption("Sudoku Game")
icon = pygame.image.load("pastime.png")
pygame.display.set_icon(icon)

# Inserting the typed number
def insert(win, position):
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont("verdana", 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(original_grid[i-1][j-1] != 0):
                    return
                if event.key == pygame.K_SPACE:
                    solver(win)
                if(event.key == 48): #checking with 0
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(screen, Background_color, (position[0]*50 + 5, position[1]*50+ 5,50 -2*5 , 50 - 2*5))
                    pygame.display.update()
                    return
                if(0 < event.key - 48 <10):  #We are checking for valid input
                    pygame.draw.rect(screen, Background_color, (position[0]*50 + 5, position[1]*50+ 5,50 -2*5 , 50 - 2*5))
                    value = myfont.render(str(event.key-48), True, new_color)
                    screen.blit(value, (position[0]*50 +15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                    
                return



def is_empty(num):
    if num == 0:
        return True
    return False



def is_valid(num,position):
     #Check for Column, row and sub-grid
    
    #Checking row
    for i in range(0, len(grid[0])):
        if(grid[position[0]][i] == num):
            return False
    
    #Checking column
    for i in range(0, len(grid[0])):
        if(grid[i][position[1]] == num):
            return False
    
    #Check sub-grid  
    x = position[0]//3*3
    y = position[1]//3*3
    #Gives us the box number
    
    for i in range(0,3):
        for j in range(0,3):
            if(grid[x+i][y+j]== num):
                return False
    return True


solved = 0
def solver(screen):
    myfont = pygame.font.SysFont("verdana", 35)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if is_empty(grid[i][j]):
                for k in range(1,10):
                    if(is_valid(k,(i,j))):
                        grid[i][j] = k
                        value = myfont.render(str(k),True,new_color)
                        screen.blit(value,((j+1)*50+15,(i+1)*50))
                        pygame.display.update()
                        # pygame.time.delay(5)
                        solver(screen)
                        global solved
                        if solved == 1:
                            return

                        grid[i][j] = 0
                        pygame.draw.rect(screen, Background_color, ((j+1)*50 + 5, (i+1)*50+ 5,50 -2*5 , 50 - 2*5))
                        pygame.display.update()

                return
        
    solved = 1


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def draw(screen):
    # Background colour
    # screen.fill((240, 230, 220))
    myfont = pygame.font.SysFont("verdana", 35)
    gap = WIDTH / 11
    for i in range(10):
        if i % 3 == 0:
            thick = 4
        else:
            thick = 1
        pygame.draw.line(
            screen, (0, 0, 0), (50, 50 + i * gap), (WIDTH - 50, 50 + i * gap), thick
        )
        pygame.draw.line(
            screen, (0, 0, 0), (i * gap + 50, 50), (i * gap + 50, WIDTH - 50), thick
        )

    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if grid[i][j] > 0 and grid[i][j] < 10:
                value = myfont.render(str(grid[i][j]), True, Fixed_color)
                screen.blit(value, ((j+1) * gap + 15, (i+1) * gap ))



def redraw_window(win, board, time):
    win.fill(Background_color)
    # Draw time
    fnt = pygame.font.SysFont("arialblack", 30)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 540))
    draw(win)


def main():
    # Game loop
    running = True
    start = time.time()
    # solver(screen)
    while running:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(screen, ((pos[0]) // 50, (pos[1]) // 50))
            if event.type == pygame.QUIT:
                running = False
        redraw_window(screen, grid, play_time)

        pygame.display.update()  # Update screen


main()
pygame.quit()
