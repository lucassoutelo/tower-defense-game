import pygame

class Inimigo(pygame.sprite.Sprite):
  def __init__(self, health, lista_animacao, x, y, speed):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.speed = speed
    self.health = health
    self.lista_animacao = lista_animacao
    self.frame_index = 0
    self.action = 2
    self.update_time = pygame.time.get_ticks()

    #selecionar imagem inicial
    self.image = self.lista_animacao[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)

  def update(self, surface):
    self.update_animacao()

    surface.blit(self.image, self.rect)

  def update_animacao(self):
    ANIMATION_COOLDOWN = 50
    self.image = self.lista_animacao[self.action][self.frame_index]
    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1
    if self.frame_index >= len(self.lista_animacao[self.action]):
      self.frame_index = 0

