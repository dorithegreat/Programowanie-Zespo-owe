from enum import Enum
import sys
from unidecode import unidecode

class buildinprognames(Enum):
    NOTATNIK = "gnome-text-editor"
    PRZEGLADARKA = "gnome-www-browser"
    PLIKI = "xdg-open ~"
    KALKULATOR = "gnome-calculator"
    TERMINAL = "gnome-terminal"
    KALENDARZ = "gnome-calendar"
    USTAWIENIA = "gnome-control-center"
    FILMY = "totem"
    LIBREOFFICE = "libreoffice"
    ZDJECIA = "shotwell -c"


def similarity(text1: str,text2: str):
    if len(text2) == 0:
        return len(text1)
    if len(text1) == 0:
        return len(text2)
    if text1[0] == text2[0]:
        return similarity(text1[1:],text2[1:])
    return 1 + min(similarity(text1[1:],text2[1:]),similarity(text1[1:],text2),similarity(text1,text2[1:]))

def LCS(text1:str,text2:str):
    C = [[0]*(len(text2) + 1)]*(len(text1)+1)
    for i in range(len(text1)):
        for j in range(len(text2)):
            if text1[i] == text2[j]:
                C[i+1][j+1] = C[i][j] + 1
            else:
                C[i+1][j+1] = max(C[i+1][j],C[i][j+1])
    return len(text1) + len(text2) - 2 * C[len(text1)][len(text2)]

def get_exact_prog_name(name: str):
        name = unidecode(name).strip().lower()
        res = "default"
        val = sys.maxsize
        for i in buildinprognames:
            print(i)
            temp = LCS(name,i.name.lower())
            if temp < val:
                val = temp
                res = i.value
        if val > 2:
            return name
        return res