import sys

prijelazi = {'<program>' : [[['<lista_naredbi>'], ['IDN', 'KR_ZA', '']]],
'<lista_naredbi>' : [[['<naredba>', '<lista_naredbi>'] , ['IDN', 'KR_ZA']],[['$'] , ['KR_AZ', '']]],
'<naredba>' : [[['<naredba_pridruzivanja>'] , ['IDN']],[['<za_petlja>'] , ['KR_ZA']]],
'<naredba_pridruzivanja>' : [[['IDN', 'OP_PRIDRUZI', '<E>'] , ['IDN']]],
'<za_petlja>' : [[['KR_ZA', 'IDN', 'KR_OD', '<E>', 'KR_DO', '<E1>', '<lista_naredbi>', 'KR_AZ'] , ['KR_ZA']]],
'<E>' : [[['<T>', '<E_lista>'], ['IDN', 'BROJ', 'OP_PLUS', 'OP_MINUS', 'L_ZAGRADA']]],
'<E1>' : [[['<T>', '<E_lista>'], ['IDN', 'BROJ', 'OP_PLUS', 'OP_MINUS', 'L_ZAGRADA']]],
'<E_lista>' : [[['OP_PLUS', '<E>'] , ['OP_PLUS']],[['OP_MINUS', '<E>'] , ['OP_MINUS']],[['$'], ['IDN', 'KR_ZA', 'KR_DO', 'KR_AZ', 'D_ZAGRADA KR']]],
'<T>' : [[['<P>', '<T_lista>'] , ['IDN', 'BROJ', 'OP_PLUS', 'OP_MINUS', 'L_ZAGRADA']]],
'<T_lista>' : [[['$'] , ['IDN', 'KR_ZA', 'KR_DO', 'KR_AZ', 'OP_PLUS', 'OP_MINUS', 'D_ZAGRADA' '']], [['OP_PUTA', '<T>'] , ['OP_PUTA']],[['OP_DIJELI', '<T>'] , ['OP_DIJELI']]],
'<P>' : [[['OP_PLUS', '<P>'] , ['OP_PLUS']],[['OP_MINUS', '<P>'] , ['OP_MINUS']],[['L_ZAGRADA', '<E>', 'D_ZAGRADA'] , ['L_ZAGRADA']],[['IDN'] , ['IDN']],[['BROJ'] , ['BROJ']]]}



class Node:

    def __init__(self, node_name):
        self.node_name = node_name

    child_nodes = []

    def add_node(self, node):
        self.child_nodes.append(node)

def print_tree(node, level):
    for n in list(node.keys()):
        if n != '<E1>':
            print(f'{" "*level}{n}')
        else:
            print(f'{" " * level}<E>')
        if '<' in n:
            if node[n] == {}:
                print(f'{" "*(level + 1)}$')
            else:
                print_tree(node[n], level + 1)



def rekurzivni_spust(node, new_state, l, index):
    line = l[index].split(' ')
    kw = line[0]
    state = new_state
    for prijelaz in prijelazi[state]:
        if kw in prijelaz[1]:
            #print(kw)
            #print(prijelaz)
            for new_node in prijelaz[0]:
                if kw == new_node and '<' not in new_node:
                    node[state][f'{line[0]} {line[1]} {line[2]}'] = ''
                    index += 1
                    line = l[index].split(' ')
                    kw = line[0]
                elif '<' not in new_node and kw != new_node and kw != '' and new_node != '$':
                    print(f'err {line[0]} {line[1]} {line[2]}')
                    return -1
                elif '<' in new_node and kw != new_node:
                    node[state][new_node] = {}
                    new_state = new_node
                    index = rekurzivni_spust(node[state], new_state, l, index)
                    if index == -1:
                        return -1
                    line = l[index].split(' ')
                    kw = line[0]
                elif new_node == '':
                    print(f'err kraj')
                    return -1
            break
    return index


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

    l = [line.strip() for line in l]
    l.append('')

    index = 0

    gen_tree = {'<program>':{}}
    success = rekurzivni_spust(gen_tree, '<program>', l, index)

    #print(gen_tree)

    if success != -1:
        print_tree(gen_tree, 0)


if __name__ == "__main__":
    main()