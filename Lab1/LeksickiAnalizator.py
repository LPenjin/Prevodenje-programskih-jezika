import sys

def get_input():
    l = []
    for line in sys.stdin:
        l.append(line)
    return l

def replace_special_chars(line, result):
    line = list(line)
    for r in result:
        for i in range(r[1], r[1] + len(r[0])):
            line[i] = ' '

    return ''.join(line)

def main():
    l = get_input()

    special_chars = {'=':'OP_PRIDRUZI',
                     '+': 'OP_PLUS',
                     '-': 'OP_MINUS',
                     '*': 'OP_PUTA',
                     '/': 'OP_DIJELI',
                     '(': 'L_ZAGRADA',
                     ')': 'D_ZAGRADA',
                     'za': 'KR_ZA',
                     'od': 'KR_OD',
                     'do': 'KR_DO',
                     'az': 'KR_AZ'}

    for line in range(len(l)):
        #rjesava komentare:
        result = []
        if '//' in l[line]:
            line_wok = l[line].split('//')[0]
        else:
            line_wok = l[line]
        first_index = 0
        for char in special_chars.keys():
            i = 0
            while (place := line_wok[i:].find(char)) != -1 and i < len(line_wok):
                i += place + len(char)
                if char.isalnum():
                    if i - 1 > 0 and i + 1 < len(line_wok):
                        if line_wok[i - 1] == ' ' and line_wok[place + len(char)] == ' ':
                            result.append([char, i - len(char)])
                    elif i - 1 > 0 and i + 1 >= len(line_wok):
                        if line_wok[i - 1] == ' ':
                            result.append([char, i - len(char)])
                    elif i - 1 < 0 and i + 1 < len(line_wok):
                        if line_wok[i - 1] == ' ':
                            result.append([char, i - len(char)])
                    else:
                        result.append([char, i - len(char)])
                else:
                    result.append([char, i - len(char)])

        line_wok = replace_special_chars(line_wok, result)

        #print(line_wok)
        state = 0
        digit_bool = False
        for i in range(len(line_wok)):
            if (line_wok[i] == ' ' or line_wok[i] == '\n' or line_wok[i].isdigit() != digit_bool) and state:
                state = 0
                end = i
                result.append([line_wok[start:end].strip(), start])
            elif state and i == len(line_wok) - 1:
                state = 0
                end = i
                result.append([line_wok[start:end + 1].strip(), start])
            if line_wok[i] != ' ' and not state:
                state = 1
                digit_bool = line_wok[i].isdigit()
                start = i


        result.sort(key= lambda x: x[1])

        for res in result:
            if res[0] in special_chars.keys():
                print(f"{special_chars[res[0]]} {line + 1} {res[0]}")
            else:
                if res[0].isdigit():
                   print(f"BROJ {line + 1} {res[0]}")
                else:
                    print(f"IDN {line + 1} {res[0]}")

        #print(result)


if __name__ == "__main__":
    main()
