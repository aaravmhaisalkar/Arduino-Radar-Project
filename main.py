import serial
import time
import pygame
import math
import queue
import threading


def MainRadar(center, radius,start,end):
    points = []
    h,k = center
    for i in range(start, end):
        x = h + math.cos(math.radians(i)) * radius
        y = k + math.sin(math.radians(i)) * radius
        points.append((x,y))
    return points

def RadarSegments(center, start, end, arc):
    points = []
    h,k = center

    for i in range(arc, (151)):
        for y in range(start,end):
            x = h + math.cos(math.radians(y)) * i
            y = k + math.sin(math.radians(y)) * i
            points.append((x,y))
    return points

task_queue = queue.Queue()
portName = "/dev/cu.usbmodem101"
coms = serial.Serial(port=portName, baudrate=115200)
time.sleep(2)
pygame.init()
points = MainRadar((200,75),150, 0, 180)
screen = pygame.display.set_mode((400,300), pygame.RESIZABLE)
pygame.display.set_caption("Radar")

def getData():
    try:
        while True:
            data = coms.readline()
            task_queue.put(data.decode('utf-8').rstrip())

            
    except KeyboardInterrupt:
        coms.close()

    task_queue.join()
    print("All tasks completed!")

thread = threading.Thread(target=getData,daemon=True)
thread.start()

running = True
forward = True
count = 0
while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill((0,0,0))
        pygame.draw.polygon(screen, "light green", points)
        
        if forward:
            count += 1
            if count >= 180:
                forward = False
        elif not forward:
            count -= 1
            if count <= 0:
                forward = True
        item = int(task_queue.get())
        if item >= 150:
            item = 150
        
        if item !=0:
            pygame.draw.polygon(
                screen,
                "red",
                RadarSegments(
                    (200,75),
                    count,
                    (count+5),
                    item
                )
            )
    finally:
        task_queue.task_done()    
    
    pygame.display.flip()
pygame.quit()



