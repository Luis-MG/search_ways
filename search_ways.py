import pygame
import random
import threading
import time
from tkinter import messagebox, Tk
from collections import deque


# Ventana y celdas
width, height = 800, 800
num_xcell = 20
num_ycell = 20
dim_xcell = width / num_xcell
dim_ycell = width / num_ycell
screen = pygame.display.set_mode((height,width))

# Predador
predator_pos = [20,20]
predator_color = [255,0,0]
pmove_step = 40
predator_speed = 0.001

# Presa
presa_pos = [740,740]
presa_color = [0,0,255]

# Matriz celdas
bloque_pos = []

queue, visited = deque(), []
path = []

start = None
end = None

class nodo:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        
    def show(self, win, col, shape= 1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x*dim_xcell, self.y*dim_ycell, dim_xcell-1, dim_ycell-1))
        else:
            pygame.draw.circle(win, col, (self.x*dim_xcell+dim_xcell//2, self.y*dim_ycell+dim_ycell//2), dim_xcell//3)
    
    def add_neighbors(self, grid):
        if self.x < num_ycell - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < num_xcell - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])


def drawCircle(color, pos):
    pygame.draw.circle(screen, color, pos, 15)

def move_x(val, character):
    if val < 0:
        for i in range(0,abs(val),1):
            character[0] = character[0] - 1
            drawCircle(predator_color,character)
            time.sleep(predator_speed)
    else:
        for i in range(0,val,1):
            character[0] = character[0] + 1
            drawCircle(predator_color,character)
            time.sleep(predator_speed)
    
        
def move_y(val, character):
    if val < 0:
        for i in range(0,abs(val),1):
            character[1] = character[1] - 1
            drawCircle(predator_color,character)
            time.sleep(predator_speed)
    else:
        for i in range(0,val,1):
            character[1] = character[1] + 1
            drawCircle(predator_color,character)
            time.sleep(predator_speed)

def move_predator(i,x_ant,y_ant):
    # print(f'x : {i.x} , y : {i.y}')
    # print(f'x_ant : {x_ant} , y_ant : {y_ant}')
    if x_ant < i.x:
        # move_x(pmove_step,predator_pos)  
        draw_tx = threading.Thread(target=move_x, args=(pmove_step,predator_pos))
        draw_tx.start()  
    if x_ant > i.x:
        # move_x(-pmove_step,predator_pos)  
        draw_tx = threading.Thread(target=move_x, args=(-pmove_step,predator_pos))
        draw_tx.start()          
    elif y_ant < i.y:
        # move_y(pmove_step,predator_pos)
        draw_ty = threading.Thread(target=move_y, args=(pmove_step,predator_pos))
        draw_ty.start()
    elif y_ant > i.y:
        # move_y(pmove_step,predator_pos)
        draw_ty = threading.Thread(target=move_y, args=(-pmove_step,predator_pos))
        draw_ty.start()                
        
    time.sleep(0.06) 


def init_matrix(num_xcell,num_ycell,bloque_pos):
    global start
    global end
    global predator_pos
    predator_pos = [20,20]
    path.clear()
    bloque_pos.clear()
    queue.clear()
    for i in range(num_xcell):
        arr = []
        for j in range(num_ycell):
            arr.append(nodo(i, j))
        bloque_pos.append(arr)

    for i in range(num_xcell):
        for j in range(num_ycell):
            bloque_pos[i][j].add_neighbors(bloque_pos)

    for x in range(num_xcell):
        for y in range(num_ycell):
            rand = bool(random.getrandbits(1))
            rand2 = bool(random.getrandbits(1))
            if rand and rand2:
                bloque_pos[x][y].wall = 1
                


    start = bloque_pos[0][0] # posicion nodo inicio 0,0
    end = bloque_pos[18][18] # posicion nodo final
    start.wall = False
    end.wall = False

    queue.append(start)
    start.visited = True
    

def draw_grid():
    for x in range(num_xcell):
        for y in range(num_ycell):
            poly = [ ( x * dim_xcell, y * dim_ycell),
                    ((x + 1) * dim_xcell, y * dim_ycell),
                    ((x + 1) * dim_xcell, (y + 1) * dim_ycell),
                    ( x * dim_xcell, (y + 1) * dim_ycell)
            ]
            
            if bloque_pos[x][y].wall == 0:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 1 )
            else:
                pygame.draw.polygon(screen, (100, 100, 100), poly, 0)
            
            pygame.draw.polygon(screen, (128, 128, 128), poly, width=1)



def main():
    init_matrix(num_xcell,num_ycell,bloque_pos)

    print(bloque_pos[0][0])

    pygame.init()
    bg = (255, 255, 255)
    pygame.display.set_caption("Search Ways")
    flag = False
    noflag = True
    startflag = False

    Tk().wm_withdraw()
    messagebox.showinfo(message="Presione:\n ENTER - Para iniciar busqueda\n R - Para recrear mapa", title="Alerta !")

    while True:

        for event in pygame.event.get():  # the for event loop, keeping track of events,
            if event.type == pygame.QUIT:  # and in this case, it will be keeping track of pygame.QUIT, which is the X or the top right
                pygame.quit()  # stops pygame
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    draw_tx = threading.Thread(target=move_x, args=(pmove_step,predator_pos))
                    draw_tx.start()                         
                if event.key == pygame.K_LEFT:
                    draw_tx = threading.Thread(target=move_x, args=(-pmove_step,predator_pos))
                    draw_tx.start()      
                if event.key == pygame.K_UP:
                    draw_ty = threading.Thread(target=move_y, args=(-pmove_step,predator_pos))
                    draw_ty.start()    
                if event.key == pygame.K_DOWN:
                    draw_ty = threading.Thread(target=move_y, args=(pmove_step,predator_pos))
                    draw_ty.start()    
                if event.key == pygame.K_RETURN:
                    startflag = True
                if event.key == pygame.K_r:
                    flag = False
                    noflag = True
                    startflag = False
                    init_matrix(num_xcell,num_ycell,bloque_pos)
                    
        
        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Ruta encontrada")
                        startflag = False
                        
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    print("No hay ruta")
                    noflag = False
                    Tk().wm_withdraw()
                    messagebox.showinfo(message="No existe una ruta, presione la tecla r para recrear el mapa", title="Alerta !")
                else:
                    continue

        screen.fill(bg)
        
        for i in range(num_ycell):
            for j in range(num_xcell):
                nodo = bloque_pos[i][j]
                # Pinta ruta
                if nodo in path:                   
                    nodo.show(screen, (46, 204, 113))
                    #nodo.show(screen, (192, 57, 43), 0)
                elif nodo.visited and not startflag:
                    nodo.show(screen, (255, 255, 255))
                elif nodo.visited:
                    nodo.show(screen, (39, 174, 96))             
        
        if flag:
            path.reverse()
            x_ant = path[0].x
            y_ant = path[0].y
            for i in path:
                move_predator(i,x_ant,y_ant)
                screen.fill(bg)
                for a in range(num_ycell):
                    for j in range(num_xcell):
                        nodo = bloque_pos[a][j]
                        # Pinta ruta
                        if nodo in path:                   
                            nodo.show(screen, (46, 204, 113))         
                draw_grid()
                drawCircle(predator_color,predator_pos)
                drawCircle(presa_color,presa_pos)
                pygame.display.flip()
                x_ant = i.x
                y_ant = i.y                  
        flag = False

        draw_grid()

        drawCircle(predator_color,predator_pos)
        drawCircle(presa_color,presa_pos)
           
    

        pygame.display.flip()
    

main()    
