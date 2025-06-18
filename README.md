# Bot Minimax w Pythonie

## Autor

- **Imię i nazwisko:** Mikolaj Chicinski
- **index:** 272337
- Pliki w C (serwer i gracz) zostały napisane przez Profesora Macieja Gębałe.

## Opis projektu

Projekt to bot gracza napisany w języku Python, który wykorzystuje algorytm minimax do podejmowania decyzji w grze. Bot łączy się z serwerem gry za pomocą gniazd sieciowych i reaguje na otrzymywane dane wejściowe, symulując i wybierając najlepszy możliwy ruch na podstawie zadanej głębokości przeszukiwania.

## Użyte biblioteki i ich zastosowanie

W programie wykorzystano wyłącznie standardowe biblioteki Pythona:

- **`socket`**  
  Umożliwia połączenie z serwerem gry za pomocą protokołu TCP/IP oraz obsługę komunikacji (wysyłanie i odbieranie danych).
  
- **`sys`**  
  Służy do pobierania argumentów z linii komend, takich jak adres IP serwera, port, numer gracza, nazwa gracza i głębokość algorytmu minimax.
  
- **`random`**  
  Pomaga w podejmowaniu losowych decyzji, np. przy wyborze jednego z równoważnych ruchów lub jako fallback w przypadku braku sensownego ruchu.
  
- **`time`**  
  Wykorzystywana do mierzenia czasu działania lub wprowadzenia opóźnień (opcjonalnie, np. w debugowaniu lub dla ograniczeń czasowych serwera).

Nie są wymagane żadne zewnętrzne paczki — wszystko opiera się na standardowej bibliotece Pythona.

## Instalacja na czystym Ubuntu

Na czystym systemie Ubuntu wystarczy zainstalować Pythona:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```
nie ma potrzeby instalowac dodatkowych paczek do pyhona

## Odpalanie

python3 my_python_bot.py <IP_SERWERA> <PORT> <NUMER_GRACZA> <NAZWA_GRACZA> <GŁĘBOKOŚĆ_MINIMAX>
