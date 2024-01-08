# Pacman Project
 **I. Co realizuje projekt**

Projekt realizuje grę Pacman. Po uruchomieniu programu możemy wybrać opcje start new game i rozpocząć rozgrywkę pacmana, sterując strzałkami poruszamy pacmanem tak, aby zjadał kropki i nie dał się złapać duchom. Gdy duch dogoni Pacmana wszystkie postaci wracają na początkowe pozycje i Pacman traci jedno życie. Za zjedzenie jednej małej kropki otrzymuje 10 punktów, a do wygrania gry musi zjeść wszystkie małe kropki. Po zjedzeniu większej kropki gracz zdobywa 50 punktów i aktywuję się specjalny tryb gry, w którym duchy zmieniają kolor, spowalniają i Pacman może wtedy zjeść takiego ducha. Takie działanie wynagradza gracza 200 punktami oraz chwilą odpoczynku od goniących go duchów(wracają na określony czas do domku na środku planszy). Za zjedzenie wszystkich dużych kropek Pacman dostaje dodatkowe życie. Oprócz prowadzenia rozgrywki użytkownik może, klinknąc przycisk Menu i wrócić do pierwszej planszy programu. Wtedy może wznowić rozgrywkę przyciskiem Resumu, co spowoduje powrót do ostatnio prowadzonej gry. Kolejną opcją jest zapis stanu gry, gdy użytkownik kliknie przycisk save game na terminalu pojawi się komenda prosząca o podanie nazwy pod jaką ma zapisać stan gry. Program blokuje wpisanie pustej nazwy, a gdy użytkownik poda nazwę pod którą jakiś stan już był zapisany prosi o potwierdzenie i ostrzega o nadpisaniu tamtego stanu. Kolejną możliwością jest klinknięcie przycisku load game w menu i załadowanie poprzednio zapisanych stanów gry. Wtedy terminal wyświetla nazwy możliwych stanów do wczytania lub informuje o braku zapisanych stanów. Wtedy użytkownik wpisuje w terminal, który stan chciałby wczytać, a program weryfikuje czy taki stan istnieje.
Ostatnim przyciskiem w menu jest exit co pozwala wyłaczyć grę.


**II. Jak go uruchomić, zainstalować dependencje**
Należy sklonować repozytorium. Wejść do katalogu pacman. Wpisać w terminal pip install -r requirements.txt, aby pobrać pygame. Kolejnym krokiem jest wpisanie python3 main.py i wtedy okienko z grą się wyświetli na ekranie.


**III. diagram architektury projektu z opisem tej architektury**

**Postawowe elementy gry.**

_Klasa Character_ - posiada atrybuty takie jak położenie na planszy (x,y), szybkość postaci, promień, który określa wielkość postaci oraz prywatna zmienną angle, która definiuje, w które stronę postać idzie. 

_Klasa Pacman_ - dziedziczy po Character, dodatkowo posiada atrybut lives, który określa ile żyć Pacmanowi zostało. Ma również atrubuty takie jak kąt otwarcia buzi i kierunek ruchu ust, dzięi którym funkcja animate_mouth sprawia że pacman rusza ustami. Kolejna funkcja go home wykorzystywana jest gdy Pacman umiera i wraca na pozycję. Draw - rysuje na ekranie.

_Klasa Ghost_ - dziedziczy po Character, dodatkowo duchy mają imiona, i zmienne określające w którym stanie są(w domu, wychodzą, przestraszone, nieżywe). Klasa posiada funkcje pozwalające na zmianę kierunku ruchu wraz z ustawieniem swojej kolejnej komórki, co wykorzystuje algorytm sterujący duchami.

_Klasa Board_ - posiada planszę i ma funkcję odpowiadajace na pytania czy w danym miejscu jest coś na planszy

_Klasa Points_ - klasa liczy zwykłe i super punkty oraz informuję klasę gry gdy super punkt zostanie zjedzony i trzeba właczyć inny tryb gry.


**Klasy pomagające zarządzać zewnętrznymi elementami gry**

_Klasa EventHandler_ - reaguję na kliknięcia strzałek przez użytkownika i  przycisku button

_Klasa Renderer_ - sprawia że wszystkie elementy gry pojawiają się na odpowiednich powierzchniach


**Klasy zarządzające logiką gry**

_Cell Logic_ - posiada funkcje pozwalające obliczać potrzebne komórki do algorytmów zarządzających grą

_Element Mover_ dzidziczy po Cell Logic i korzystając z jej i swoich funkcji rusza obiektami zgodnie z kierunkiem i pilnuje by nie wjeżdzały w ściany.

_GhostDetectingWalls_ - dziedziczy po cell logic i w inny sposób oblicza dla ducha, w które kierunki są dostępne dla jego algorytmu. Ma tez funkcje distance, która dostarcza potrzebne wartosci do algorytmu, wybierającego kierunek ducha. Funkcja collision na dwa sposoby sprawdza czy duch i pacman sie nie zdeżyli.

_Klasa NormalGhostAction_ - sklada sie z funkcji go_to_tile, ktora jest podstawa kazdego ruchu ducha. Oblicza do ktorej nastepnej komórki bardziej opłaca się iść duchowi. Funckje scatter i chase sa zaimplementowane zgodnie z zasadami orginalnego pacmana z artykułu https://gameinternals.com/understanding-pac-man-ghost-behavior , który dokładnie określa jak w pacmanie duchy wytyczają swoje trasy. Tryb scatter powoduje ze każdy duch idzie do swojego ustawionego kąta, tryb chase powoduje, że duchy gonią pacmana na różny sposób w zależności od ich osobowości co też jest opisane w artykule powyżej. Funkcja run powoduje, że duchy co określoną liczbę sekund zmieniają tryby i kierunki, co sprawia, że gra jest trudniejsza.

_Klasa FrightenedGhostAction_ - korzysta z klasy ghost logic ktora dostarcza w która stronę duch nie może iść i randomowo wybiera kierunek. Oraz zarządza zmianami w zachowaniu duchów w tym trybie.

_Klasa DeadGhostAction_ korzysta z algorytmu z klasy NormalGhostAction i diedziczy po niej i odpowiada za ruch duchów, które zjadł pacman by wróciły do domku.


**Klasa Game**
Klasa która zarządza wszystkimi poniższymi klasami, łączy elemnty gry, logikę i komunikację z użytkownikiem i powierzchniami.


**Klasy pomocnicze dla menu** 

_Klasa Serializer_ - ważne elementy gry wyciąga z klas do słowników by zapisać do pliku

_Klasa Deserializer_ - z słowników odtwarza elementy gry i pozwala wznowić grę z zapisanego stanu


**Klasy Menu**

_Klasa button_ odpowiada za wygląd przycisku, wykrywanie czy został klknięty i przechowywanie, która funkcja  z klasy Menu powinna byc wykonana po jego kliknięciu.

_Klasa Menu_ odpowiada za akcję które dzieją się po wciśnięciu przycisku czyli rozpoczęcia, wznowienie gry, zapisu i odczytu z pliku. Oraz klasa przechowuję obecny stan gry, który był ostatnio rozwgrywany lub żadny jeśli jeszcze nie grano. Klasa zarządza co się dzieję z klasą Game.


**Podsumowanie architektury**

Podstawowe elemnety gry + Klasy pomagające zarządzać grą + Klasy pomagające zarządzać zewnętrznymi elementami gry = **Game**

Button + Game + Klasy pomocnicze dla menu = **Menu**



