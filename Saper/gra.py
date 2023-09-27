import pygame
import random
import queue


from plansza import Plansza

class Gra():
    
    def __init__(self, plansza, rozmiarEkranu):
        self.plansza = plansza
        self.rozmiarEkranu = rozmiarEkranu
        self.rozmiarPola = (self.rozmiarEkranu[0] // self.plansza.getRozmiar(), self.rozmiarEkranu[1] // self.plansza.getRozmiar())
        self.ladowanieObrazow()


    def start(self):
        pygame.init()
        pygame.display.set_caption('Saper - Projekt J.Marzec, A.Krzykała') # ustawienie nazwy okna
        self.ekran = pygame.display.set_mode(self.rozmiarEkranu) #utworzenie okna o odpowiednim rozmiarze
        self.stanGry = "Start"
        isRunning = True
        self.rysuj()
        while isRunning:
            for zdarzenie in pygame.event.get():
                if zdarzenie.type == pygame.QUIT: #przerwanie gry
                    isRunning = False
                if zdarzenie.type == pygame.MOUSEBUTTONDOWN:
                    klikLewy = pygame.mouse.get_pressed()[0] #funkcja pobierajaca event klikniecia lewego przycisku myszy
                    if(klikLewy):
                        if self.stanGry == "Start": 
                            self.rozpocznij(pygame.mouse.get_pos()) 
                            self.stanGry = "W trakcie" 
                        elif self.stanGry == "W trakcie":
                            self.klikniecieLewy(pygame.mouse.get_pos())
                        elif self.stanGry == "Koniec":
                            self.plansza = Plansza(self.plansza.rozmiar, self.plansza.liczbaBomb)
                            self.rysuj()
                            self.stanGry = "Start"
                    
                            
                    klikPrawy = pygame.mouse.get_pressed()[2] #funkcja pobierajaca event klikniecia prawego przycisku myszy
                    if(klikPrawy):
                        if self.stanGry == "W trakcie":
                            self.kliknieciePrawy(pygame.mouse.get_pos()) 
            pygame.display.update() #odswiezenie widoku okna
        pygame.quit() #zamkniecie okna
        
        
    def rysuj(self):
        przesuniecie = (self.rozmiarEkranu[0] - self.plansza.getRozmiar() * self.rozmiarPola[0])//2 # wyliczenie liczby pikseli ktore zostaly przy dzieleniu rozmiaru ekranu
        LGRog = (przesuniecie,przesuniecie) # ustalenie punktu rozpoczecia wstawiania zdjecia pustych pól
        for wiersz in range(self.plansza.getRozmiar()):
            for kolumna in range(self.plansza.getRozmiar()):
                self.ekran.blit(self.polePuste, LGRog) #wpisanie w odpowiednie miejsce obrazka pustego pola
                LGRog = (LGRog[0] + self.rozmiarPola[0], LGRog[1]) # Przejscie po kolumnach 
            LGRog = (przesuniecie, LGRog[1] + self.rozmiarPola[1]) # Przejscie do kolejnego wiersza
    
    
    def ladowanieObrazow(self):
        self.listaPol = [] # lista do pól 0-8
        
        for i in range(9): #load i transfor do odpowiedniej rozdzielczosci oraz dodanie do listy pól 0-8
            sciezka = "Pola/"+str(i)+".png"
            pole = pygame.image.load(sciezka)
            pole = pygame.transform.scale(pole, self.rozmiarPola)
            self.listaPol.append(pole)

        self.polePuste = pygame.image.load("Pola/puste.png") # load i transform pola pustego
        self.polePuste = pygame.transform.scale(self.polePuste, self.rozmiarPola)
        
        self.flaga = pygame.image.load("Pola/flaga.png") # load i transform pola flagi
        self.flaga = pygame.transform.scale(self.flaga, self.rozmiarPola)
        
        self.bomba = pygame.image.load("Pola/bomba.png") # load i transform pola bomby
        self.bomba = pygame.transform.scale(self.bomba, self.rozmiarPola) 
        
        self.bomba2 = pygame.image.load("Pola/bomba2.png") # load i transform pola bomby wybuchającej
        self.bomba2 = pygame.transform.scale(self.bomba2, self.rozmiarPola) 
        
        self.poleKoniec = pygame.image.load("Pola/planszaKoniec.png") # load pola koniec
        self.poleWygrana = pygame.image.load("Pola/planszaWygrana.png")
        
        
    def klikniecieLewy(self, pozycja): #metoda do obslugi klikniecia lewym przyciskiem myszy
        pos = pozycja[1] // self.rozmiarPola[1], pozycja[0] // self.rozmiarPola[0] #wylicza komorke w tablicy gry
        czyBomba = self.plansza.plansza[pos[0]][pos[1]].czyBomba
        czyFlaga = self.plansza.plansza[pos[0]][pos[1]].czyFlaga
        czyOdkryty = self.plansza.plansza[pos[0]][pos[1]].czyOdkryty
        if czyFlaga:
            return
        else:
            if czyOdkryty:
                return
            else:
                if czyBomba == True: #jezeli klikniesz w bombe to wyswietla wszystkie bomby na planszy i konczy gre
                    for X in range(self.plansza.rozmiar):
                        for Y in range(self.plansza.rozmiar):
                            if self.plansza.plansza[X][Y].czyBomba:
                                self.zmienObrazek(self.bomba, (X,Y))
                    self.zmienObrazek(self.bomba2, pos)
                    self.stanGry = "Koniec"
                    self.zmienObrazek(self.poleKoniec, (0,0))
                    return
                else: 
                    self.plansza.odznacz((pos[0], pos[1]))
                    self.zmienObrazek(self.listaPol[self.plansza.plansza[pos[0]][pos[1]].sumaBomb], pos) #odkrycie pola 
                    if self.plansza.plansza[pos[0]][pos[1]].sumaBomb == 0: #jesli suma bomb wokol pola jest rowna 0 to odkrywa pobliskie pola
                        q = queue.Queue()
                        q.put((pos))
                        while not q.empty():
                            element = q.get()
                            self.zmienObrazek(self.listaPol[self.plansza.plansza[element[0]][element[1]].sumaBomb], element)
                            if self.plansza.plansza[element[0]][element[1]].sumaBomb == 0:
                                for X in range(-1,2):
                                    for Y in range(-1,2):
                                        if X == 0 and Y == 0: 
                                            break
                                        elif X + element[0] in range(self.plansza.rozmiar) and Y + element[1] in range(self.plansza.rozmiar):
                                            if self.plansza.plansza[X + element[0]][Y + element[1]].czyOdkryty == False:
                                                q.put((X + element[0], Y + element[1]))
                                                self.plansza.odznacz((X + element[0], Y + element[1]))
        if self.plansza.liczbaBomb == self.plansza.liczbaNieodkryte: #warunek wygrania gry
            self.stanGry = "Koniec"
            self.zmienObrazek(self.poleWygrana, (0,0))
    
    
    def kliknieciePrawy(self, pozycja): #obsluga flagowania pol
        pos = pozycja[1] // self.rozmiarPola[1], pozycja[0] // self.rozmiarPola[0]
        czyFlaga = self.plansza.plansza[pos[0]][pos[1]].czyFlaga
        czyOdkryty = self.plansza.plansza[pos[0]][pos[1]].czyOdkryty
        if czyOdkryty:
            return
        else:#zamienia pole na flage lub zwykle pole 
            self.plansza.plansza[pos[0]][pos[1]].czyFlaga = not self.plansza.plansza[pos[0]][pos[1]].czyFlaga
            if self.plansza.plansza[pos[0]][pos[1]].czyFlaga == True:
                self.zmienObrazek(self.flaga, pos)
            else:
                self.zmienObrazek(self.polePuste, pos)
        
    
    def rozpocznij(self, pozycja): #przygotowanie planszy do gry
        pos = pozycja[1] // self.rozmiarPola[1], pozycja[0] // self.rozmiarPola[0]
        rozmiar = self.plansza.rozmiar
        liczbaBomb = self.plansza.liczbaBomb
        licznik = 0
        while licznik < liczbaBomb: #rozmieszczenie bomb
            X = random.randint(0, rozmiar-1)
            Y = random.randint(0, rozmiar-1)
            if (X == pos[0] and Y == pos[1]) == False:
                if self.plansza.plansza[X][Y].czyBomba == False:
                    self.plansza.plansza[X][Y].czyBomba = True
                    licznik += 1
        self.plansza.liczBomby() 
        self.klikniecieLewy(pozycja)
        
        
    def zmienObrazek(self, obrazek, pozycja): #ustawia podany obrazek na dane pole
        przesuniecie = (self.rozmiarEkranu[0] - self.plansza.getRozmiar() * self.rozmiarPola[0])//2 # wyliczenie liczby pikseli ktore zostaly przy dzieleniu rozmiaru ekranu
        pos = pozycja[1] * self.rozmiarPola[1] + przesuniecie,  pozycja[0] * self.rozmiarPola[0] + przesuniecie
        self.ekran.blit(obrazek, pos)
