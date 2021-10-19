import sys


def main():
    print('Ja sam retardiran sto sam odabrao tezu inacicu')
    predlozak = open('predlozak.txt', 'r')
    predlosci = predlozak.readlines()
    predlozak_pocetak = ''
    predlozak_string = ''
    stringovi = {}
    novi_predlozak = True
    print(predlosci)
    for i in range(len(predlosci)):
        if (predlosci[i]) != '\n':
            if novi_predlozak:
                novi_predlozak = False
                predlozak_pocetak = predlosci[i].strip()
            else:
                predlozak_string = predlozak_string + predlosci[i]
                print(predlozak_pocetak)
                print(predlozak_string)
        else:
            print(predlozak_pocetak)
            stringovi[predlozak_pocetak] = predlozak_string
            predlozak_string = ''
            novi_predlozak = True
    print(stringovi)
    file = open('analizator/LA.py', 'w')
    file.write(stringovi['pocetak'])

    l = []
    for line in sys.stdin:
        l.append(line)
    print(l)
    reg_def = {}
    imena_stanja = []
    imena_lex_jedinki = []
    stanje = 0
    for i in range(l):
        if stanje == 0:
            if l[i][0] == '{':
                temp = l[i].split(' ')
                reg_def_name = temp[0].replace('{', '').replace('}', '')
                reg_def_list = temp[1].split('|')
                reg_def[reg_def_name] = reg_def_list
            else:
                stanje = 1
        if stanje == 1:
            if l[i].startswith('%X'):
                temp = l[i].strip()[3:].split(' ')
                imena_stanja = temp
            else:
                stanje = 2
        if stanje == 2:
            if l[i].startswith('%L'):
                temp = l[i].strip()[3:].split(' ')
                imena_lex_jedinki = temp
            else:
                stanje = 3
        if stanje == 3:





    file.write(stringovi['zavrsetak'])
    file.close()


if __name__ == '__main__':
    main()