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
            temp = int(korak.split()[1])
            index = index - temp
        elif korak != '-':
            print(korak, red, match)

    return red, novo_stanje, index


def is_multiple_matches(match_list):
    starting_pos = 100000000000000000000000
    ending_pos = -1
    max_match = 0

    #Finds the starting and ending index
    for i in range(len(match_list)):
        if match_list[i][2][0] < starting_pos:
            starting_pos = match_list[i][2][0]
        if match_list[i][2][1] > ending_pos:
            ending_pos = match_list[i][2][1]

    l = [0 for i in range(ending_pos-starting_pos)]
    k = [0 for i in range(ending_pos-starting_pos)]

    #Marks which letters are used by multiple regexes
    for match in match_list:
        for i in range(match[2][0] - starting_pos, match[2][1] - starting_pos):
            l[i] += 1

    #Marks which letter are used by what regex
    for j in range(len(match_list)):
        for i in range(match_list[j][2][0] - starting_pos, match_list[j][2][1] - starting_pos):
            k[i] = j + 1

    imp_sum = l[-1] + k[-1]
    last_regex = k[-1]
    i = len(l) - 1
    #Checks if there are regexes that are not overlapping
    while i > -1:
        temp_sum = l[i] + k[i]
        if temp_sum != imp_sum:
            for match in range(len(match_list)):
                if max_match < match_list[match][2][1] - match_list[match][2][0]:
                    max_match = match_list[match][2][1] - match_list[match][2][0]
                    match_index = match
            if match_list[match_index] != match_list[-1]:
                return match_index
            else:
                return 0
        if last_regex != k[i]:
            return None
        i += -1

    #print('l', l)
    #print('k', k)


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
    #print(l)
    #print(prijelazi)
    for prijelaz in prijelazi.values():
        for value in prijelaz:
            if value[0] == '\_':
                value[0] = ' '
    for line in range(len(l)):
        match_list = []
        for stanje_it in prijelazi.keys():
                for prijelaz in prijelazi[stanje_it]:
                    offset = 0
                    while first_index + offset < len(l[line]):
                        #print(index)
                        if x := re.search(prijelaz[0], l[line][first_index + offset:]):
                            new_offset = offset + x.span()[1]
                            span = []
                            span.append(x.span()[0] + offset)
                            span.append(x.span()[1] + offset)
                            offset = new_offset
                            match_list.append([x, prijelaz, span])
                        else:
                            offset += 1
        match_list.sort(key=lambda x: x[2])
        #print(match_list)

        match_list_overlap = []
        overlapping = []
        for i in range(len(match_list)):
            if match_list[i] not in overlapping:
                overlap = [match_list[i]]
                for j in range(len(match_list)):
                    if match_list[j][2][0] >= match_list[i][2][0] and match_list[j][2][1] <= match_list[i][2][1] and j != i:
                        overlap.append(match_list[j])
                        overlapping.append(match_list[j])
                    elif match_list[i][2][0] >= match_list[j][2][0] and match_list[i][2][1] <= match_list[j][2][1] and j != i:
                        continue
                match_list_overlap.append(overlap)

        print(match_list_overlap)

        for i in range(len(match_list_overlap)):
            solve_match(match_list_overlap[i][0][1], l[line]
            [match_list_overlap[i][0][2][0]:match_list_overlap[i][0][2][1]],
                                             line + 1, 0, stanje)
        max_match = 0
        max_match_index = 0
        """
        for match in range(len(match_list)):
            if max_match < match_list[match][2][1] - match_list[match][2][0]:
                max_match = match_list[match][2][1] - match_list[match][2][0]
                max_match_index = match

        if len(match_list) >= 2:
            match_list.sort(key = lambda x: x[2])
            match_index = is_multiple_matches(match_list)
            if match_index != None:
                #print('Puno je elemenata')
                red, stanje, index = solve_match(match_list[match_index][1], match_list[match_index][0].string
                [match_list[match_index][2][0]:match_list[match_index][2][1]],
                                                 red, index, stanje)
                first_index += match_list[match_index][2][1]

    if match_list:
        max_match = 0
        max_match_index = 0

        for match in range(len(match_list)):
            if max_match < match_list[match][0].endpos - match_list[match][0].pos:
                max_match = match_list[match][0].endpos - match_list[match][0].pos
                max_match_index = match

        red, stanje, index = solve_match(match_list[max_match_index][1], match_list[max_match_index][0].string
        [match_list[max_match_index][2][0]:match_list[max_match_index][2][1]],
                                         red, index, stanje)"""



if __name__ == "__main__":
    main()
