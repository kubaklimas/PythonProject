import pygame, sys, random
#
from os import path


class Gracz (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,50))
        self.image.set_colorkey((0, 0, 0)) # usuwanie ddddddczarnej ramki w okół png
        self.rect = self.image.get_rect()
        self.v = 0
        self.pion = 0
        self.rect.x = 300
        self.rect.y = 300
    def update(self):  #fizyka gracza
        self.v = 0
        self.pion
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.v += 5
        elif keys[pygame.K_a]:
            self.v -= 5
        elif keys[pygame.K_w]:
            self.pion -= 0.5
        elif keys[pygame.K_s]:
            self.pion += 0.5
        #pozycja
        self.rect.x+=self.v
        self.rect.y+=self.pion

        # ściany
        if self.rect.right > 1280:
            self.rect.right = 1280
        elif self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom >720:
            self.rect.bottom = 720
    def dokumentacja(self):
        """
        W klasie opisany jest wygląd, oraz cała fizyka gracza. Predkosci poziome i pionowe, współczynniki
        predkości, ograniczenia aby gracz nie mógł wylecieć poza sciane
        argumenty i co zwraca
        """
        pass

class Przeciwnik(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img,(50,50))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1200)
        self.rect.y = random.randint(0, 700)
        self.predkosc = 3
        self.predkoscpion = 3
    def update(self):  #fizyka moba
        self.rect.y = self.rect.y + self.predkoscpion
        self.rect.x = self.rect.x + self.predkosc
        if self.rect.x > 1250:
            self.predkosc = - self.predkosc
        if self.rect.x < 0 :
            self.predkosc = - self.predkosc
        elif self.rect.y >690:
            self.predkoscpion = - self.predkoscpion
        elif self.rect.y <0:
            self.predkoscpion = - self.predkoscpion

    def dokumentacja(self):
        """
        W klasie opisany jest wygląd przeciwników, ich rozmieszczenie, oraz fizyka ich poruszania i ograniczeń
        """
        pass



FPS = 60
pygame.init() # do fps
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Prison Break")
clock = pygame.time.Clock()

# tlo / wrog / gracz
tlo = pygame.image.load("pygame.png").convert()
tlo_rect = tlo.get_rect()
player_img = pygame.image.load("player.png").convert()
enemy_img = pygame.image.load("enemy.png").convert()


sprajty = pygame.sprite.Group() #przypisanie wszystkich Sprite do grupy
player = Gracz() # Respienie gracza na mapie
sprajty.add(player)
enemies = pygame.sprite.Group() # Wrogowie do grupy (collide)
for i in range (10) :
    e = Przeciwnik()
    sprajty.add(e)
    enemies.add(e)

    # Pętla gry, jak false przerywa
running = True
while running:
    # wyświetlaj w 60 klatkach na sek
    clock.tick(FPS)
    # zdarzenia
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    # Update
    sprajty.update()
    smierc = pygame.sprite.spritecollide(player, enemies, False)
    if smierc:
        running = False
    # Rysuj / usuwaj
    screen.fill((0,0,0))
    screen.blit(tlo, tlo_rect)
    sprajty.draw(screen)

    pygame.display.flip()

pygame.quit()

