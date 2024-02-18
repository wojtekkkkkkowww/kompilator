## KOMPILATOR JFTT 
Wojciech Kowalczyk 268486

### Środowisko
* Python - v.```3.10.12```
* sly - v.```0.5```
Do systemu Ubuntu należy doinstalowac biblioteke sly 
np. ``` pip install sly ```
### Pliki
* ```Lexer.py``` - lexer
* ```Parser.py``` - parser
* ```Analyzer.py``` - klasa szukająca błędów w programie
* ```CodeGenerator.py``` -plik generujący kod maszynowy
* ```Definitions.py``` - plik z pomocniczymi klasami  
* ```PseudoCode.py ``` - pomocnicze funkcje 
* ```kompilator.py``` - kompilator

### Użycie
linux:
```python3 kompilator.py <input> <output> ```