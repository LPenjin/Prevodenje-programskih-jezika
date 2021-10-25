import sys
from tablica import Tablica
import re

def solve_match(prijelaz, match, red, index, stanje):
    novo_stanje = stanje
    for korak in prijelaz[1:]:
        if korak == 'NOVI_REDAK':
            red += 1
        elif korak.startswith('UDJI_U_STANJE'):
            temp = korak.split()[1]
            novo_stanje = temp
        elif korak.startswith('VRATI_SE'):
            temp = korak.split()[1]
            index = index - temp
        elif korak != '-':
            print(korak, red, match)

    return red, novo_stanje, index


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
    red = 1
    first_index = 0
    l = ''.join(l)
    print(l)
    last_match_list = []
    for index in range(len(l)):
        match_list = []
        for prijelaz in prijelazi[stanje]:
            if x := re.search(prijelaz[0], l[first_index:index]):
                match_list.append([x, prijelaz])
        max_match = 0
        max_match_index = 0

        for match in range(len(match_list)):
            if max_match < match_list[match][0].span()[1] - match_list[match][0].span()[0]:
                max_match = match_list[match][0].span()[1] - match_list[match][0].span()[0]
                max_match_index = match

        if len(match_list) > 2:
            for i in range(len(match_list)):
                if match_list[i][0].span()[1] == index and match_list[max_match_index][0].span()[1] < match_list[i][0].span()[0]:
                    first_index = index - 1
                    red, stanje, index = solve_match(match_list[max_match_index][1], match_list[max_match_index][0].string
                    [match_list[max_match_index][0].span()[0]:match_list[max_match_index][0].span()[1]],
                                                     red, index, stanje)
        if len(last_match_list) == len(match_list):
            for last_match in last_match_list:
                for match in match_list:
                    if match[0].re.pattern == last_match[0].re.pattern and match[0].regs == last_match[0].regs:
                        first_index = index - 1
                        #print(match_list[max_match_index].span()[0], match_list[max_match_index].span()[1])
                        red, stanje, index = solve_match(match_list[max_match_index][1], match_list[max_match_index][0].string
                        [match_list[max_match_index][0].span()[0]:match_list[max_match_index][0].span()[1]],
                                                         red, index, stanje)

        last_match_list = match_list.copy()

    if match_list:
        max_match = 0
        max_match_index = 0

        for match in range(len(match_list)):
            if max_match < match_list[match].endpos - match_list[match].pos:
                max_match = match_list[match].endpos - match_list[match].pos
                max_match_index = match

        red, stanje, index = solve_match(match_list[max_match_index][1], match_list[max_match_index][0].string
        [match_list[max_match_index][0].span()[0]:match_list[max_match_index][0].span()[1]],
                                         red, index, stanje)



if __name__ == "__main__":
    main()
