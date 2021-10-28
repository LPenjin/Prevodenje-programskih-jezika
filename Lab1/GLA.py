import sys
import re

def get_input():
    l = []
    for line in sys.stdin:
        l.append(line)
    return l

def escape_chars(string):
    return string

def main():
    predlozak = open('predlozak.txt', 'r')
    predlosci = predlozak.readlines()
    predlozak_pocetak = ''
    predlozak_string = ''
    stringovi = {}
    novi_predlozak = True
    #Tu se ucitavaju predlosci
    for i in range(len(predlosci)):
        if (predlosci[i]) != '\n':
            if novi_predlozak:
                novi_predlozak = False
                predlozak_pocetak = predlosci[i].strip()
            else:
                predlozak_string = predlozak_string + predlosci[i]
        else:
            stringovi[predlozak_pocetak] = predlozak_string
            predlozak_string = ''
            novi_predlozak = True

    #Otvaranje fajla za analizator
    file = open('analizator/tablica.py', 'w')
    file.write(stringovi['pocetak'])

    #Upisivanje svih linija u jednu listu
    l = get_input()

    #Unosenje iz ulazne datoteke u podatkovne strukture
    reg_def = {}
    imena_lex_jedinki = []
    stanje = 0
    prijelazi = {}
    operacija = []
    for i in range(len(l)):
        if stanje == 0:
            if l[i][0] == '{':
                temp = l[i].split(' ')
                reg_def_name = temp[0].replace('{', '').replace('}', '')
                reg_def_list = temp[1].strip()
                reg_def[reg_def_name] = reg_def_list
                reg_def[reg_def_name] = escape_chars(reg_def[reg_def_name])
            else:
                stanje = 1
        if stanje == 1:
            if l[i].startswith('%X'):
                temp = l[i].strip()[3:].split(' ')
                pocetno_stanje = temp[0]
                for s in temp:
                    prijelazi[s] = []
            else:
                stanje = 2
        if stanje == 2:
            if l[i].startswith('%L'):
                temp = l[i].strip()[3:].split(' ')
                imena_lex_jedinki = temp
            else:
                stanje = 3
        if stanje == 3:
            if l[i].startswith('<'):
                temp = l[i].strip().replace('<', '').replace('>', ' ').split(' ')
                prijelaz = [temp[1].replace('$', '')]
                stanje_prijelaza = temp[0]
            elif l[i].startswith('{'):
                stanje = 4
                continue
        if stanje == 4:
            if not l[i].startswith('}'):
                prijelaz.append(l[i].strip())
            else:
                stanje = 3
                prijelazi[stanje_prijelaza].append(prijelaz)

    for definition in reg_def.keys():
        if x := re.findall('{[a-zA-Z]*}', reg_def[definition]):
            for match in x:
                reg_def[definition] = reg_def[definition].replace(match, f'({reg_def[match[1:-1]]})')

    for stanje in prijelazi.keys():
        for prijelaz in range(len(prijelazi[stanje])):
            if x := re.findall('{[a-zA-Z]*}', prijelazi[stanje][prijelaz][0]):
                for match in x:
                    prijelazi[stanje][prijelaz][0] = prijelazi[stanje][prijelaz][0].replace(match, f'({reg_def[match[1:-1]]})')


    #debug stuff
    print('Reg_def ', reg_def)
    print('Imena ',imena_lex_jedinki)
    print('prijelazi', prijelazi)

    file.write(stringovi['Tablica'])
    file.write('\tpocetno_stanje = ' + '\'' + pocetno_stanje + '\'' + '\n')
    file.write('\tReg_def = ' + str(reg_def) + '\n')
    file.write('\tImena = ' + str(imena_lex_jedinki) + '\n')
    file.write('\tprijelazi = ' + str(prijelazi) + '\n')
    file.write(stringovi['zavrsetak'])
    file.close()


if __name__ == '__main__':
    main()