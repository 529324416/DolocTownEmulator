import time
import random
import threading


import pygame

# def main():
#     screen = pygame.display.set_mode((300,400))

#     while 1:
#         screen.fill(0)
#         pygame.display.flip()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit(0)
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 print('用户按下了a键')

# t = threading.Thread(target=main)
# t.start()

# while 1:
#     time.sleep(1)
#     print('main thread is running now')

for i in range(100):
    print(random.randint(1,10))