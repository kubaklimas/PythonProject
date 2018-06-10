import pygame, sys, random
#
from os import path


class Gracz (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,50))
        self.image.set_colorkey((0, 0, 0)) # usuwanie czarnej ramki png
        self.rect = self.image.get_rect()
        self.radius = 25
        self.v = 0
        self.pion = 0
        self.rect.centerx = width/2
        self.rect.bottom = heigth - 50
    def update(self):  #fizyka gracza
        self.v = 0

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

    def strzal(self):

        ammo = Strzal(self.rect.centerx, self.rect.bottom)
        sprajty.add(ammo)
        bullets.add(ammo)


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
        self.radius = 25
        self.rect.x = random.randint(0, 1200)
        self.rect.y = 25
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
        elif self.rect.y <-50:
            self.predkoscpion = - self.predkoscpion

    def dokumentacja(self):
        """
        W klasie opisany jest wygląd przeciwników, ich rozmieszczenie, oraz fizyka ich poruszania i ograniczeń
        """
        pass

class Strzal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.predkosc = -5

    def update(self):
        self.rect.y += self.predkosc
        if self.rect.bottom < 0:
            self.kill()
czcionka  = pygame.font.match_font('arial')
def wypisz(wyglad, text, rozmiar, x, y):
    font = pygame.font.Font(czcionka,rozmiar)
    tekst = font.render(text,True,(255, 0, 0))
    tekst_rect = tekst.get_rect()
    tekst_rect.midtop = (x,y)
    wyglad.blit(tekst,tekst_rect)

def ekran():
    wypisz(screen, "Try to kill 1000 aliens, GL & HF", 50, width / 2, heigth / 4 + 110)
    wypisz(screen, "Press any button to start the game", 50, width / 2, heigth / 4 + 165)
    pygame.display.flip()
    czekaj = True
    while czekaj:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                czekaj = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()




FPS = 60
pygame.init() # do fps
pygame.mixer.init()
width = 1280
heigth = 720
screen = pygame.display.set_mode((width, heigth))
pygame.display.set_caption("Shot'em all")
clock = pygame.time.Clock()

# tlo / wrog / gracz
tlo = pygame.image.load("pygame.png").convert()
tlo_rect = tlo.get_rect()
player_img = pygame.image.load("player.png").convert()
enemy_img = pygame.image.load("enemy.png").convert()




lvlhard = 0
running = True
start = True
    # Pętla gry, jak false przerywa

while running:
    if start:
        ekran()
        start = False
        sprajty = pygame.sprite.Group()  # przypisanie wszystkich Sprite do grupy
        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()  # Wrogowie do grupy (collide)
        player = Gracz()  # Respienie gracza na mapie
        sprajty.add(player)
        ilosc_gr = 3
        punkty = 0

        for i in range(ilosc_gr):
            e = Przeciwnik()
            sprajty.add(e)
            enemies.add(e)

    # wyświetlaj w 60 klatkach na sek
    clock.tick(FPS)
    # zdarzenia
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.strzal()
    lvlhard =  lvlhard+1
    if lvlhard%300 == 0:
        a = Przeciwnik()
        sprajty.add(a)
        enemies.add(a)
    # Update
    sprajty.update()
    smierc = pygame.sprite.spritecollide(player, enemies, False,pygame.sprite.collide_circle)
    kill = pygame.sprite.groupcollide(bullets,enemies,True,True)
    for ded in kill:
        punkty +=1
        a = Przeciwnik()
        sprajty.add(a)
        enemies.add(a)
    if smierc:
        start = True
    # Rysuj / usuwaj
    screen.fill((0,0,0))
    wypisz(screen,str(punkty),15,width/2,heigth-20)

    screen.blit(tlo, tlo_rect)
    sprajty.draw(screen)

    pygame.display.flip()

pygame.quit()


