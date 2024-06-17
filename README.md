# Program do niwelowania szumów w obrazach in vivo uzyskanych przy użyciu techniki Power Doppler

## Procedura uruchomienia programu:
- w przypadku braku zainstalowanego python (co najmniej wersja 3.12) zainstaluj lub zaktualizuj go zgodnie z instrukcją zamieszczoną na oficjalnej stronie pythona https://www.python.org/downloads/
- włącz terminal
- przejdź do katalogu w którym znajduje się wcześniej pobrany program
- wpisz poniższą komendę
  
```
python program.py <ścieżka względna lub bezwzględna do pliku wejściowego z rozszerzeniem .dcm> <(opcjonalnie) nazwa pliku wyjściowego z rozszerzeniem .dcm> <(opcjonalnie) ręczne ustawienie wartości granicznej>
```

Przykładowe komendy (system Windows 10):
- `python program.py C:\\dane_wejsciowe\\dane_wejsiowe_1.dcm C:\\dane_wysciowe\\dane_wyjsciowe_1.dcm 2000000` - program przeanalizuje "plik dane_wejsiowe_1.dcm" znajdujący się w katalogu "C:\\dane_wejsciowe", przy wartości granicznej równej 2 000 000, a następnie zapisze odszumiony plik pod nazwą "dane_wyjsciowe_1.dcm" w katalogu "C:\\dane_wysciowe" (przy założeniu że plik wejściowy i dane katalogi istnieją)
- `python program.py C:\\dane_wejsciowe\\dane_wejsiowe_1.dcm C:\\dane_wysciowe\\dane_wyjsciowe_1.dcm` - program ustawi wartość graniczną na 1 000 000 (wartość domyślna)
- `python program.py C:\\dane_wejsciowe\\dane_wejsiowe_1.dcm` - program zapisze plik wyjściowy jako datę np "2024-06-10 17-54-08.dcm" w katalogu w którym znajduje się program i ustawi wartość graniczną na 1 000 000 (wartość domyślna)

Dodatkowe informacje o uruchamianiu programu:
- W przypadku braku wpisania wartości granicznej program automatycznie ustawi wartość na 1 000 000
- W przypadku braku wpisania pliku wejściowego program stworzy plik o mający jako nazwę aktualną datę np. "2024-06-10 17-54-08.dcm"
- Nie jest możliwe ustawienie wartości granicznej bez podania nazwy pliku wyjściowego!
