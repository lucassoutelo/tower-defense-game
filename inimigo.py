import pygame

class Inimigo(pygame.sprite.Sprite):
  def __init__(self, health, lista_animacao, x, y, speed):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.speed = speed
    self.health = health
    self.lista_animacao = lista_animacao
    self.frame_index = 0
    self.action = 0
    self.update_time = pygame.time.get_ticks()

    #selecionar imagem inicial
    self.image = self.lista_animacao[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)

  def update(self, surface, target, grupo_balas):
    if self.alive:
      #checar colisão com balas
      if pygame.sprite.spritecollide(self, grupo_balas, True):
        #diminuir vida do inimigo
        self.health -= 25

      #checar se inimigo chegou a torre
      if self.rect.right > target.rect.left:
        self.action = 1

      #movimentar inimigo
      if self.action == 0:
        self.rect.x += self.speed

      #checar se a vida chegou a 0
      if self.health <= 0:
        target.ouro += 100
        target.pontos += 1
        self.update_action(2)
        self.alive = False

    self.update_animacao()

    surface.blit(self.image, self.rect)

  def update_animacao(self):
    ANIMATION_COOLDOWN = 50
    self.image = self.lista_animacao[self.action][self.frame_index]
    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1
    if self.frame_index >= len(self.lista_animacao[self.action]):
      if self.action == 2:
        self.frame_index = len(self.lista_animacao[self.action]) - 1
      else: 
        self.frame_index = 0

  def update_action(self, new_action):
    #checa se a acao é diferente da anterior
    if new_action != self.action:
      self.action = new_action
      #atualiza as animações
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()
