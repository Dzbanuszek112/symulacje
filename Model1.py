
#                        MODEL 1 - Gaz idealny


# Import bibliotek
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
from random import choices
from random import sample
import math 


def ustawienie_pola(N, ncol, nrow):
    '''
    Tworzy startową "macierz planu" - pole symulacji.
    
    Argumenty:
    N: Liczba cząstek w symulacji.
    ncol: Ilosc kolumn macierz planu.
    nrow: Ilosc wierszy macierzy planu.
    
    Zwraca macierz planu oraz obliczoną granicę.
    '''
    
    # tworzę macierz planu
    wezly = nrow*ncol
    macierz_planu = np.zeros(wezly)
    macierz_planu=macierz_planu.reshape((nrow, ncol))
    
    # losuję współrzędne punktów startowych
    if ncol%2==0:
        granica = int(ncol/2) # czyli od granicy (wlacznie) mamy prawą stronę - numeracja od 0
        losowe_X=choices(range(granica), k=N) # losowanie ze zwracaniem
        losowe_Y=choices(range(nrow), k=N) # losowanie ze zwracaniem
    else:
        granica=int((ncol-1)/2) # granicą jest dosłownie srodkowa kolumna
        losowe_X=choices(range(granica), k=N)
        losowe_Y=choices(range(nrow), k=N)
    
    # nakładamy punkty startowe
    for i in range(N):
        if macierz_planu[losowe_Y[i],losowe_X[i]] == 0:
            macierz_planu[losowe_Y[i],losowe_X[i]] = 1
        else:
            macierz_planu[losowe_Y[i],losowe_X[i]] += 1
    
    # Wylosowanie jednego zaznaczonego punktu.
    indeks = sample(range(N), k=1)
    dot=[]
    Dot_x = losowe_X[indeks[0]]
    Dot_y = losowe_Y[indeks[0]]
    dot.append(Dot_x)
    dot.append(Dot_y)

    return macierz_planu, granica, dot



def dyspersja(ncol, nrow, macierz_planu):
    '''
    Funkcja dokonująca przestawień punktów na macierzy planu.
    
    Argumenty:
        ncol: ilosć kolumn w macierzy planu
        nrow: ilosć wierszy w macierzy planu
        macierz_planu: macierz definiująca plan pola

    Zwraca macierz z losowo przestawionymi punktami.
    '''
    wezly = nrow*ncol # ilosć pól w macierzy
    nowa_macierz = (np.zeros(wezly)).reshape((nrow, ncol))
    kierunki = list(range(1,5)) # 1: w lewo, 2: w prawo, 3: w dół, 4: w górę
    L = 0 # ogranicznik przesunięć Blue Dota
    
    # iterowanie po macierzy planu
    for i in range(ncol): # aktualizacja po kolumnach od lewej strony
        for j in range(nrow):
            if macierz_planu[j,i] != 0:
                nowa_pozycja = [j, i]
                for p in range(int(macierz_planu[j,i])): # iterujemy tyle razy ile punktów w pozycji
                    kierunek_skoku=choices(kierunki, k=1) # losujemy jedną liczbę
                    
                    if kierunek_skoku[0] == 1: # w lewo
                        if i-1 < 0:
                            nowa_macierz[j,i]+=1
                        elif ncol%2!=0 and i-1 == int((ncol-1)/2):
                            nowa_macierz[j,i-2]+=1
                            nowa_pozycja=[j, i-2]
                        else:
                            nowa_macierz[j,i-1]+=1
                            nowa_pozycja=[j, i-1]
                    
                    elif kierunek_skoku[0] == 2: # w prawo
                        if i+1 > ncol-1:
                            nowa_macierz[j,i]+=1
                        elif ncol%2!=0 and i+1 == int((ncol-1)/2):
                            nowa_macierz[j,i+2]+=1
                            nowa_pozycja=[j, i+2]
                        else:
                            nowa_macierz[j,i+1]+=1
                            nowa_pozycja=[j,i+1]
                    
                    elif kierunek_skoku[0] == 3: # w dół
                        if j+1 > nrow-1:
                            nowa_macierz[j,i]+=1
                        else:
                            nowa_macierz[j+1,i]+=1
                            nowa_pozycja=[j+1, i]
                    
                    elif kierunek_skoku[0] == 4: # w górę
                        if j-1 < 0:
                            nowa_macierz[j,i]+=1
                        else:
                            nowa_macierz[j-1,i]+=1
                            nowa_pozycja=[j-1, i]
                
                if i == blue_dot[0] and j == blue_dot[1] and L==0:
                    #print(przesuniecie)
                    blue_dot[0]=nowa_pozycja[1]
                    blue_dot[1]=nowa_pozycja[0]
                    L += 1

    return nowa_macierz



def wspolrzedne(ncol, nrow, macierz): 
    # obliczenie współrzędnych w nowej macierzy
    wspolrzedne_X = list()
    wspolrzedne_Y = list()  
    for i in range(ncol):
        for j in range(nrow):
            if macierz[j,i] != 0:
                wspolrzedne_X.append(i)
                wspolrzedne_Y.append(j)
        
    return wspolrzedne_X, wspolrzedne_Y



def entropia(N, macierz_planu, granica):
    '''
    Funkcja oblicza wartosć logarytmu dziesiętnego
    entropii konfiguracyjnej.
    
    Argumenty:
        N: ilosć cząstek w symulacji
        macierz_planu: macierz reprezentująca pole symulacji
        granica: indeks kolumny granicznej (między lewą a prawą stroną)
    
    Zwraca logarytm dziesiętny entropii konfiguracyjnej.
    '''
    podmacierz = macierz_planu[:,:granica] # tylko lewa strona macierzy planu
    NL= int(sum(sum(podmacierz))) # zliczenie cząstek po lewej stronie
    NP=int(N-NL) # obliczenie cząstek po prawej stronie
    sigma = math.factorial(N)/(math.factorial(NL)*math.factorial(NP)) # entropia konfiguracyjna
    return math.log(sigma, 10)



def porzadek(N, macierz_planu, granica):
    '''
    Funkcja oblicza wartosć fenomenologicznego parametru porządku.
    
    Argumenty:
        N: ilosć cząstek w symulacji
        macierz_planu: macierz reprezentująca pole symulacji
        granica: indeks kolumny granicznej (między lewą a prawą stroną)
    
    Zwraca wartosć fenomenologicznego parametru porządku.
    '''
    podmacierz = macierz_planu[:,:granica] # tylko lewa strona macierzy planu
    NL= int(sum(sum(podmacierz))) # zliczenie cząstek po lewej stronie
    NP=int(N-NL) # obliczenie cząstek po prawej stronie
    p = (NL-NP)/N # fenomenologiczny parametr porządku
    return p  

#%% Częsć graficzna i scalająca


def main(ilosc_iteracji, ncol, nrow, N, opoznienie):
    '''
    Funkcja główna wykonująca symulację.
    
    Argumenty:
        ilosc_iteracji: Ilosć kroków symulacji.
        ncol: Szerokosc pola symulacji.
        nrow: Wysokosć pola symulacji.
        N: Ilosć cząstek w symulacji.
        szybkosc: Ilosć czasu w milisekundach pomiędzy kolejnymi iteracjami.
    '''
    # Sprawdzenie argumentów:
    assert ilosc_iteracji > 0, "Ilosć iteracji powninna być większa niż zero!"
    assert type(ilosc_iteracji) == int, "Ilosć iteracji powninna być liczbą całkowitą!"
    assert ncol > 0, "Szerokosć pola symulacji powninna być wieksza niż zero!"
    assert type(ncol) == int, "Szerokosć pola symulacji powninna być liczbą całkowitą!"
    assert nrow > 0, "Wysokosć pola symulacji powinna być większa niż zero!"
    assert type(nrow) == int, "Wysokosć pola symulacji powninna być liczbą całkowitą!"
    assert N > 0, "Ilosć cząstek powinna być większa niż zero!"
    assert type(N) == int, "Ilosć cząstek powninna być liczbą całkowitą!"
    assert opoznienie > 0, "Opoźnienie symulacji powinno być większe niż zero!"
    assert type(opoznienie) == int, "Opoźnienienie symulacji powninno być liczbą całkowitą!"
    
    
    # Definiuję zmienne globalne
    global macierz_planu, granica, sigma, Por, anim, blue_dot
    macierz_planu, granica, blue_dot = ustawienie_pola(N, ncol, nrow)
    sigma=list()
    Por=list()
    wspolrzedne_X, wspolrzedne_Y = wspolrzedne(ncol, nrow, macierz_planu)
    sigma.append(entropia(N, macierz_planu, granica))
    Por.append(porzadek(N, macierz_planu, granica))
    anim=[0]

    
    # Animacja
    def animate(i, ncol, nrow):
        global macierz_planu, granica, sigma, iteracja, Por, blue_dot
        #print(blue_dot)
        
        # Aktualizacja informacji o macierzy i pozycji cząstek.
        macierz_planu = dyspersja(ncol, nrow, macierz_planu)
        wspolrzedne_X, wspolrzedne_Y = wspolrzedne(ncol, nrow, macierz_planu)
        
        # Aktualizacja wykresu pozycji cząstek.
        sc.set_offsets(np.c_[wspolrzedne_X, wspolrzedne_Y])
        
        # Aktualizacja pozycji blue dota.
        BD.set_offsets(np.c_[blue_dot[0], blue_dot[1]])
        
        # Aktualizacja danych o entropii i porządku.
        sigma.append(entropia(N, macierz_planu, granica))
        Por.append(porzadek(N, macierz_planu, granica))
        
        # Aktualizacja wykresu entropii.
        ax2.clear()
        ax2.plot(sigma, label='Entropia')
        ax2.legend(loc='lower right')
        ax2.set_xlabel('Iteracje')
        ax2.set_ylabel(r'$\sigma$')
        ax2.set_title('Entropia w czasie')
        
        # Aktualizacja wykresu porzadku.
        ax3.clear()
        ax3.plot(Por, label='Porządek')
        ax3.legend(loc='upper right')
        ax3.set_xlabel('Iteracje')
        ax3.set_ylabel('P')
        ax3.set_title('Porządek w czasie')
    
    # Styl wykresów i układ wykresów.
    plt.style.use('ggplot')
    
    fig = plt.figure(figsize=(12, 9)) # 12-szerokosć, 9-wysokosć (w calach)
    fig.tight_layout(pad=5.0)
    gs = fig.add_gridspec(ncols=2, nrows=2)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    
    
    # Stworzenie wykresu dla entropii.
    line1, = ax2.plot(sigma)
    ax2.set_title('Entropia w czasie')
    ax2.set_ylabel(r'$\sigma$')
    ax2.set_xlabel('Iteracje')


    # Stworzenie wykresu dla pozycji cząstek.
    sc = ax1.scatter(wspolrzedne_X, wspolrzedne_Y)
    ax1.set_title('Pole dyspersji', fontsize=20)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_xlim([-1,ncol])
    ax1.set_ylim([-1,nrow])
    ax1.set_xticks(np.arange(0, ncol, 1))
    ax1.set_yticks(np.arange(0, nrow, 1))
    
    # Zaznaczenie blue dota.
    BD = ax1.scatter(blue_dot[0], blue_dot[1], s=80, facecolors='blue', edgecolors='red')


    # Stworzenie wykresu dla porządku.
    line1, = ax3.plot(Por)
    ax3.set_title('Porządek w czasie')
    ax3.set_ylabel('P')
    ax3.set_xlabel('Iteracje')
    
    
    anim[0] = matplotlib.animation.FuncAnimation(fig, animate, 
                                              frames=ilosc_iteracji, interval=opoznienie,
                                              repeat=False, fargs=(ncol, nrow)) 
    plt.show()

#%% Częsć uruchamiająca

main(ilosc_iteracji=400, ncol=20, nrow=10, N=60, opoznienie=200)


