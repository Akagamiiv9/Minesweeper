from gra import Gra
from plansza import Plansza
import math
rozmiarPlanszy = 6 #ustalenie rozmiaru planszy
procentBomb = 0.15 #procentowa wartość bomb na planszy 
liczbaBomb = math.floor(rozmiarPlanszy * rozmiarPlanszy * procentBomb)
plansza = Plansza(rozmiarPlanszy, liczbaBomb) #utworzenie planszy o odpowiednim rozmiarze X na X
rozmiarEkranu = (600,600) # ustalenie rozmiaru ekranu
gra = Gra(plansza, rozmiarEkranu) #utworzenia obiektu gry
gra.start() #rozpoczecie gry