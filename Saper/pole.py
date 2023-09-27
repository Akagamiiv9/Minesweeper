class Pole:
    def __init__(self):
        self._czyBomba = False
        self._czyOdkryty = False
        self._czyFlaga = False
        self._sumaBomb = 0
    
   #gettery i settery, sprawdzanie czy wartosc prawidlowa
    @property
    def sumaBomb(self):
        return self._sumaBomb
    @sumaBomb.setter
    def sumaBomb(self, nowa_sumaBomb):
        if type(nowa_sumaBomb) != int:
            print("Błąd typu")
        else:
          if nowa_sumaBomb>=0 and nowa_sumaBomb<=8:
              self._sumaBomb = nowa_sumaBomb   
          else:
              print("Błąd wartości")


    @property
    def czyBomba(self):
        return self._czyBomba
    @czyBomba.setter
    def czyBomba(self, nowa_czyBomba):
        if type(nowa_czyBomba) != bool:
            print("Błąd typu")
        else:
            self._czyBomba = nowa_czyBomba  
   

    @property
    def czyFlaga(self):
        return self._czyFlaga
    @czyFlaga.setter
    def czyFlaga(self, nowa_czyFlaga):
        if type(nowa_czyFlaga) != bool:
            print("Błąd typu")
        else:
            self._czyFlaga = nowa_czyFlaga 
            
    
    @property
    def czyOdkryty(self):
        return self._czyOdkryty
    @czyOdkryty.setter
    def czyOdkryty(self, nowa_czyOdkryty):
        if type(nowa_czyOdkryty) != bool:
            print("Błąd typu")
        else:
            self._czyOdkryty = nowa_czyOdkryty