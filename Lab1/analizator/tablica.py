import sys
def main():
    l = []
    for line in sys.stdin:
        l.append(line)
    print(l)
class Tablica:
	pocetno_stanje = 'S_a'
	Reg_def = {'space': '\\_', 'a': 'a', 'xyz': '(x|y|z)abc', 't': '((x|y|z)abc)(a)'}
	Imena = ['A', 'B', 'C', 'D', 'T']
	prijelazi = {'S_a': [['\\n', '-', 'NOVI_REDAK'], ['(\\_)', '-'], ['(a)', 'A'], ['((x|y|z)abc)', 'B'], ['((x|y|z)abc)((x|y|z)abc)', 'C'], ['o((x|y|z)abc)*', 'D'], ['t(((x|y|z)abc)(a))', 'T']]}
if __name__ == "__main__":
    main()
