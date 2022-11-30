import pygame
import math
import random
from inimigo import Inimigo

pygame.init()

#TAMANHO DA JANELA
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600

#VARIÁVEIS DO JOGO
level = 1
level_difficulty = 0
target_difficulty = 1000
#MAX_INIMIGOS = 10
INIMIGOS_TIMER = 1000
last_inimigo = pygame.time.get_ticks()
inimigos_vivos = 0

#CRIA JANELA
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('Defesa de torre')

clock = pygame.time.Clock()
FPS =  60

#CARREGAR IMAGENS
backgrund = pygame.image.load('img/bg4.jpg').convert_alpha()
torreimg100 = pygame.image.load('img/torre/castle_100.png').convert_alpha()
torreimg50 = pygame.image.load('img/torre/castle_50.png').convert_alpha()
torreimg25 = pygame.image.load('img/torre/castle_25.png').convert_alpha()

#Imagem de balas
bala_img =  pygame.image.load('img/bala.png').convert_alpha()
b_width = bala_img.get_width()
b_height = bala_img.get_height()
bala_img = pygame.transform.scale(bala_img, (int(b_width * 0.1), int(b_height * 0.1)))

#carregar inimigos
inimigo_animacao = []
tipos_inimigos = ['demonio', 'rato']
inimigo_vida = [40, 100]

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
  def __init__(self, image100, image50, image25, x, y, scale):
    self.health = 1000
    self.max_health = self.health
    self.fired = False
    self.ouro = 0
    self.pontos = 0

    width = image100.get_width()
    heigth = image100.get_height()

    self.image100 = pygame.transform.scale(image100, (int(width * scale), int(heigth * scale)))
    self.image50 = pygame.transform.scale(image50, (int(width * scale), int(heigth * scale)))
    self.image25 = pygame.transform.scale(image25, (int(width * scale), int(heigth * scale)))
    self.rect = self.image100.get_rect()
    self.rect.x = x
    self.rect.y = y

  def Shoot(self):
    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - self.rect.midleft[0]
    y_dist = -(pos[1] - self.rect.midleft[1])
    self.angle = math.degrees(math.atan2(y_dist, x_dist))
    
    #get mouse_click
    if pygame.mouse.get_pressed()[0] and self.fired == False:
      self.fired = True
      bala = Bala(bala_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
      grupo_balas.add(bala)
    #resetando mouseclick
    if pygame.mouse.get_pressed()[0] == False:
      self.fired = False

    #pygame.draw.line(screen, WHITE, (self.rect.midleft[0], self.rect.midleft[1]), (pos))
  
  def Draw(self):
    #checar qual imagem usar baseada na vida da torre
    if self.health <= 250:
      self.image = self.image25
    elif self.health <= 500:
      self.image =  self.image50
    else:
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
torre = Torre(torreimg100, torreimg50, torreimg25, SCREEN_WIDTH - 250, SCREEN_HEIGTH - 300, 0.2)

#CRIAR GRUPOS
grupo_balas = pygame.sprite.Group()
grupo_inimigos = pygame.sprite.Group()

#CRIAR INIMIGOS
#inimigo_1 = Inimigo(inimigo_vida[0], inimigo_animacao[0], 200, SCREEN_HEIGTH - 150, 1)
#grupo_inimigos.add(inimigo_1)

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
  grupo_inimigos.update(screen, torre, grupo_balas)

  #movimenta balas
  grupo_balas.update()

  #criar inimigos
  #checar numero max de inimigos
  if level_difficulty < target_difficulty:
    if pygame.time.get_ticks() - last_inimigo > INIMIGOS_TIMER:
      e = random.randint(0, len(tipos_inimigos) - 1)
      inimigo = Inimigo(inimigo_vida[e], inimigo_animacao[e], -100, SCREEN_HEIGTH - 150, 1)
      grupo_inimigos.add(inimigo)
      last_inimigo = pygame.time.get_ticks()
      level_difficulty += inimigo_vida[e]

  #eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

pygame.quit()