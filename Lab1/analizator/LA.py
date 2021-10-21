import sys
from tablica import Tablica
import re

def main():
    l = []
    for line in sys.stdin:
        l.append(line)

    tablica = Tablica()
    stanje = Tablica.pocetno_stanje
    reg_def = Tablica.Reg_def
    imena = Tablica.Imena
    #posebni_znakovi = Tablica.Posebni_znakovi
    prijelazi = Tablica.prijelazi

    for i in range(len(l)):
        greska = True
        for prijelaz in prijelazi[stanje]:
            if x := re.findall(prijelaz[0], l[i]):
                greska = False
                for find in x:
                    print(f"{prijelaz[1]} {i + 1} {find}")
        if greska:
            print('Ovo ne valja debilu', file=sys.stderr)

if __name__ == "__main__":
    main()
