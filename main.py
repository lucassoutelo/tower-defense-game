import pygame
import math

pygame.init()

#TAMANHO DA JANELA
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600

#CRIA JANELA
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('Defesa de torre')

clock = pygame.time.Clock()
FPS =  60

#CARREGAR IMAGENS
backgrund = pygame.image.load('img/bg4.jpg').convert_alpha()
torreimg100 = pygame.image.load('img/torre/torre100.png').convert_alpha()
bala =  pygame.image.load('img/bala.png')

#definir cores
WHITE =  (255, 255, 255)

#CLASSE TORRE
class Torre():
  def __init__(self, image100, x, y, scale):
    self.health = 1000
    self.max_health = self.health

    width = image100.get_width()
    heigth = image100.get_height()

    self.image100 = pygame.transform.scale(image100, (int(width * scale), int(heigth * scale)))
    self.rect = self.image100.get_rect()
    self.rect.x = x
    self.rect.y = y

  def Shoot(self):
    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - self.rect.midleft[0]
    y_dist = pos[1] - self.rect.midleft[1]
    self.angle = math.degrees(math.atan2(x_dist, y_dist))

    pygame.draw.line(screen, WHITE, (self.rect.midleft[0], self.rect.midleft[1]), (pos))
  
  def Draw(self):
    self.image = self.image100
    screen.blit(self.image, self.rect)

#CRIAR TORRE
torre = Torre(torreimg100, SCREEN_WIDTH - 250, SCREEN_HEIGTH - 300, 0.2)

#JOGO EM LOOP
run = True
while run:

  clock.tick(FPS)
  screen.blit(backgrund, (0,0))

  #desenha torre
  torre.Draw()
  torre.Shoot()

  #eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

pygame.quit()