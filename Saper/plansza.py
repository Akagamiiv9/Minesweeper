from pole import Pole
class Plansza():
    def __init__(self, rozmiar, liczbaBomb): 
        self.rozmiar = rozmiar
        self.ustawPlansze()
        self.liczbaBomb = liczbaBomb
        self.liczbaNieodkryte = self.rozmiar * self.rozmiar
        
        
    def ustawPlansze(self): #tworzenie planszy
        self.plansza = []
        for wiersz in range(self.rozmiar):
            wiersz = []
            for kolumna in range(self.rozmiar):
                pole = Pole()
                wiersz.append(pole)
            self.plansza.append(wiersz)
            
            
    def getRozmiar(self): #pobiera rozmiar planszy
        return self.rozmiar
    
    
    def liczBomby(self): #zliczanie bomb na sasiadujacych polach
        for wiersz in range(self.rozmiar):
            for kolumna in range(self.rozmiar):
                licznikBomb = 0
                for X in range(-1,2):
                    for Y in range(-1,2):
                        if X == 0 and Y == 0: 
                            continue
                        elif X + wiersz in range(self.rozmiar) and Y + kolumna in range(self.rozmiar):
                            if self.plansza[wiersz+X][kolumna+Y].czyBomba:
                                licznikBomb += 1
                self.plansza[wiersz][kolumna].sumaBomb = licznikBomb
            
                
    def odznacz(self, pozycja): #odkrycie pola
        self.plansza[pozycja[0]][pozycja[1]].czyOdkryty = True
        self.liczbaNieodkryte -= 1
    
