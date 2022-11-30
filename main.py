import pygame
import math
from inimigo import Inimigo

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

#Imagem de balas
bala_img =  pygame.image.load('img/bala.png').convert_alpha()
b_width = bala_img.get_width()
b_height = bala_img.get_height()
bala_img = pygame.transform.scale(bala_img, (int(b_width * 0.1), int(b_height * 0.1)))

#carregar inimigos
inimigo_animacao = []
tipos_inimigos = ['demonio']
inimigo_vida = [80]

tipos_animacoes = ['andando', 'morto', 'atacando']

for inimigos in tipos_inimigos:
  #carregar animacoes
  lista_animacoes = []
  for animacoes in tipos_animacoes:
    #resetar lista temporaria de imagens
    temp_list = []
    num_of_frames = 5
    for i in range (num_of_frames):
      img = pygame.image.load(f'img/inimigos/{inimigos}/{animacoes}/{i}.png').convert_alpha()
      temp_list.append(img)
    lista_animacoes.append(temp_list)
  inimigo_animacao.append(lista_animacoes)

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
    y_dist = -(pos[1] - self.rect.midleft[1])
    self.angle = math.degrees(math.atan2(y_dist, x_dist))
    self.fired = False
    
    #get mouse_click
    if pygame.mouse.get_pressed()[0] and self.fired == False:
      self.fired = True
      bala = Bala(bala_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
      grupo_balas.add(bala)
    #resenatndo mouseclick
    if pygame.mouse.get_pressed()[0] == False:
      self.fired = False

    #pygame.draw.line(screen, WHITE, (self.rect.midleft[0], self.rect.midleft[1]), (pos))
  
  def Draw(self):
    self.image = self.image100
    screen.blit(self.image, self.rect)

#CLASSE BALAS
class Bala(pygame.sprite.Sprite):
  def __init__(self, image, x, y, angle):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.angle = math.radians(angle)
    self.speed = 10
    self.dx = math.cos(self.angle) * self.speed
    self.dy = -(math.sin(self.angle) * self.speed)

  def update(self):
    #se a bala sair da tela
    if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGTH:
      self.kill()

    #mover a bala
    self.rect.x += self.dx
    self.rect.y += self.dy


#CRIAR TORRE
torre = Torre(torreimg100, SCREEN_WIDTH - 250, SCREEN_HEIGTH - 300, 0.2)

#CRIAR GRUPOS
grupo_balas = pygame.sprite.Group()
grupo_inimigos = pygame.sprite.Group()

#CRIAR INIMIGOS
inimigo_1 = Inimigo(inimigo_vida[0], inimigo_animacao[0], 200, SCREEN_HEIGTH - 200, 1)
grupo_inimigos.add(inimigo_1)

#JOGO EM LOOP
run = True
while run:

  clock.tick(FPS)
  screen.blit(backgrund, (0,0))

  #desenha torre
  torre.Draw()
  torre.Shoot()
  #desenha balas
  grupo_balas.draw(screen)

  #desenha inimigos
  grupo_inimigos.update(screen)

  #movimenta balas
  grupo_balas.update()

  #eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

pygame.quit()