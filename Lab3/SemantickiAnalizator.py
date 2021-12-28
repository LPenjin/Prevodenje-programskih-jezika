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
    not_found = True
    for prijelaz in prijelazi[state]:
        if kw in prijelaz[1]:
            not_found = False
            #print(kw)
            #print(prijelaz)
            for new_node in prijelaz[0]:
                if kw == new_node and '<' not in new_node:
                    node[state][f'{line[0]} {line[1]} {line[2]}'] = ''
                    index += 1
                    line = l[index].split(' ')
                    kw = line[0]
                elif '<' in new_node and kw != new_node:
                    node[state][new_node] = {}
                    new_state = new_node
                    not_found, index = rekurzivni_spust(node[state], new_state, l, index)
                    if index == -1:
                        return not_found, -1
                    if not_found and kw != '':
                        print(f'err {line[0]} {line[1]} {line[2]}')
                        return not_found, -1
                    line = l[index].split(' ')
                    kw = line[0]
            break
    return not_found, index


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


#def get_gen_tree(gen_tree, l, index, indentation):
#    curr_indent = len(l[index]) - len(l[index].lstrip())

def get_loops(l):
    loops = []
    last_opened = -1
    for line in l:
        if 'KR_ZA' in line:
            split_line = line.split(' ')
            loops.append([int(split_line[1])])
            last_opened = len(loops) - 1
        elif 'KR_AZ' in line and last_opened != -1:
            split_line = line.split(' ')
            loops[last_opened].append(int(split_line[1]))
            list_range = last_opened
            last_opened = -1
            for index in reversed(range(list_range)):
                if len(loops[index]) < 2:
                    last_opened = index
                    break
    return loops

def get_definitions(l, loops):
    definitions = {}
    for index in range(len(l)):
        if 'IDN' in l[index]:
            split_line = l[index].split(' ')
            if ('<naredba_pridruzivanja>' in l[index - 1] or 'KR_ZA' in l[index - 1]):
                l[index] = 'OBRISANA LINIJA'
                if split_line[2] not in definitions.keys():
                    definitions[split_line[2]] = []
                definitions[split_line[2]].append([int(split_line[1]), 10000000000000000])
                min_loop = 1000000000
                small_loop = []
                for loop in loops:
                    if loop[0] <= int(split_line[1]) < loop[1]:
                        if loop[1] - loop[0] < min_loop:
                            min_loop = loop[1] - loop[0]
                            small_loop = loop
                if small_loop:
                    definitions[split_line[2]][-1][1] = small_loop[1]
    return definitions

def print_semantic_analysis(definitons, loops, l):
    for index in range(len(l)):
        if 'IDN' in l[index]:
            split_line = l[index].split(' ')
            min_dist = 10000000000000
            target_def = []
            for definition in definitons[split_line[2]]:
                if definition[0] <= int(split_line[1]) < definition[1]:
                    if definition[0] == int(split_line[1]):
                        error = False
                        for loop in loops:
                            if loop == definition:
                                target_def = []
                                error = True
                                break
                        if error:
                            break
                        else:
                            continue
                    else:
                        target_def = definition
                        break
            error = False
            for definition in definitons[split_line[2]]:
                if definition[0] == int(split_line[1]):
                    for loop in loops:
                        if loop == definition:
                            target_def = []
                            error = True
                            break
                    if error:
                        break
            for loop in loops:
                if loop[0] < int(split_line[1]) < loop[1]:
                    for definition in definitons[split_line[2]]:
                        if definition == loop:
                            target_def = definition
            if target_def:
                print(f"{split_line[1]} {target_def[0]} {split_line[2]}")
            else:
                print(f"err {split_line[1]} {split_line[2]}")
                break


def main():
    l = get_input()

    l = [line.strip() for line in l]

    index = 0

    gen_tree = {}
    not_found, success = rekurzivni_spust(gen_tree, '<program>', l, index)
    #print(gen_tree)
    loops = get_loops(l)
    #print(loops)
    definitions = get_definitions(l, loops)
    #print(definitions)
    print_semantic_analysis(definitions, loops, l)



if __name__ == "__main__":
    main()