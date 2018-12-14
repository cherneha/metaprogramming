import glob
from utils import only_spaces_and_special_characters, line_beggining_spaces_edit, get_side_spaces, delete_left_right, indentation_message


def run_formatter():
    repeat = 'yes'
    while(repeat == 'yes' or repeat == 'Yes' or repeat == 'YES' or repeat == 'y'
          or repeat == 'Y' or repeat == 'так' or repeat == 'да'):
        print("What do u want, dude?")
        print("1. analyse my govnocode structure")
        print("2. structure my code normally")
        print("3. create new structuring template (bad idea though)")
        choise = 0
        while choise == 0:
            choise = int(input("choose your option (1 - 3)"))
            if choise == 1:
                print("no chances to your govnocode!!!")
                project = input("give me your shitty project dir address")
                edit_dir_files('/home/stacy/CODE/metaprogramming/EDITOR-master', 4, False, False)
            elif choise == 2:
                print("let's see if it's even possible")
                project = input("give me your shitty project dir address")
                edit_dir_files('/home/stacy/CODE/metaprogramming/EDITOR-master', 4, False, True)
            elif choise == 3:
                print("u think u can make a normal template??")
                indentation = int(input("number of spaces for indentation: "))
                answer = ''
                while answer != 'a' and answer != 'd':
                    answer = input("Add or delete spaces around operators? (a/d)")
                if answer == 'a':
                    del_operator_spaces = False
                else:
                    del_operator_spaces = True
                edit_dir_files('/home/stacy/CODE/metaprogramming/EDITOR-master', indentation, del_operator_spaces, True)
            else:
                print("well, u can't even pick an option normally")
                choise = 0

        repeat = input("Repeat?")

def analyze_code(filepath, indentation, del_operator_spaces, max_len):
    file = open(filepath, mode='r')
    code = file.readlines()
    nesting = 0
    i = 0
    in_for = 0
    for line in code:
        if len(line) > 80:
            print("In line ", i + 1, "too many characters (should be <= 80)")
        i += 1
        j = 0
        spaces = 0

        if line.find(' for ') > 0 or line.find(' for(') > 0 or line.find('for ') == 0 or line.find('for(') == 0:
            in_for += 2
        line = line.replace('\t', '    ')
        for symbol in line:
            if symbol == ' ':
                spaces += 1
            else:
                break

        for symbol in line:
            if symbol == '{':
                nesting += 1
                n = line.find('{')
                ending = line[n + 1:]
                if not only_spaces_and_special_characters(ending):
                    print("Move text after opening braces to separate line (line number ", i, ")")
                break
            elif symbol == '}':
                nesting -= 1
                needed_spaces = indentation * nesting - spaces
                indentation_message(needed_spaces, i)
                n = line.find('}')
                ending = line[n + 1:]
                if not only_spaces_and_special_characters(ending):
                    print("Move closing braces to separate line (line number ", i, ")")

                break
            elif symbol == ';':
                new_line = line_beggining_spaces_edit(indentation, spaces, nesting, line)
                if in_for > 0:
                    in_for -= 1
                else:
                    n = new_line.find(';')
                    ending = new_line[n + 1:]
                    if not only_spaces_and_special_characters(ending):
                        print("Move text after semicolon to separate line (line number ", i, ")")
                    break

        needed_spaces = indentation * nesting - spaces
        indentation_message(needed_spaces, i)






def edit_dir_files(proj_path, indentation, del_operator_spaces, edit):
    cpp_files = glob.glob(proj_path + "/*.cpp")
    for cpp_file in cpp_files:
        if edit:
            edit_code(cpp_file, indentation, del_operator_spaces)
        else:
            analyze_code(cpp_file, indentation, del_operator_spaces, 80)

def edit_code(filepath, indentation, del_operator_spaces):
    fix_indentations(filepath, indentation, True)
    fix_operator_spaces(filepath, del_operator_spaces)


def fix_indentations(filepath, indentation, edit):
    file = open(filepath, mode='r')
    code = file.readlines()
    nesting = 0
    new_doc = []
    while len(code) > 0:
        in_for = 0
        line = code.pop(0)
        spaces = 0
        if line.find(' for ') > 0 or line.find(' for(') > 0 or line.find('for ') == 0 or line.find('for(') == 0:
            in_for += 2
        line = line.replace('\t', '    ')
        for symbol in line:
            if symbol == ' ':
                spaces += 1
            else:
                break
        new_line = line_beggining_spaces_edit(indentation, spaces, nesting, line)
        for symbol in line:
            if symbol == '{':
                new_line = line_beggining_spaces_edit(indentation, spaces, nesting, line)
                nesting += 1
                n = new_line.find('{')
                ending = new_line[n + 1:]
                if not only_spaces_and_special_characters(ending):
                    print(ending)
                    code = [ending] + code
                    new_line = new_line[:(n + 1)] + '\n'
                break
            elif symbol == '}':
                nesting -= 1
                n = line.find('}')
                ending = line[n + 1:]
                new_line = line_beggining_spaces_edit(indentation, spaces, nesting, line)
                if not only_spaces_and_special_characters(ending):
                    print(ending)
                    code = [ending] + code
                    new_doc.append(' ' * indentation * nesting + '}\n');
                    new_line = new_line[:n]
                break
            elif symbol == ';':
                new_line = line_beggining_spaces_edit(indentation, spaces, nesting, line)
                if in_for > 0:
                    in_for -= 1
                else:
                    n = new_line.find(';')
                    ending = new_line[n + 1:]
                    if not only_spaces_and_special_characters(ending):
                        print(ending)
                        code = [ending] + code
                        new_line = new_line[:(n + 1)] + '\n'
                    break
        new_doc.append(new_line)

    f = open(filepath, 'w')
    f.writelines(new_doc)


def fix_operator_spaces(filepath, del_spaces):
    file = open(filepath, mode='r')
    code = file.readlines()

    new_lines = list()
    for line in code:
        prev_state = 0
        i = 0
        for symbol in line:
            new_state = (get_new_state_decider(prev_state))(symbol)
            if new_state == 2:
                if del_spaces:
                    line, erased  = delete_left_right(line, i - 2, i + 1)
                    i-= erased
                else:
                    left, right = get_side_spaces(line, i - 2, i + 1)
                    line = line[:i - 1] + left + line[i - 1] + line[i] + right + line[i + 1:]
                    i += (len(left) + len(right))
            elif new_state == 9:
                if del_spaces:
                    line, erased = delete_left_right(line, i - 2, i)
                    i -= erased
                else:
                    left, right = get_side_spaces(line, i - 2, i)
                    line = line[:i-1] + left + line[i - 1]  + right + line[i:]
                    i+=(len(left) + len(right))
            prev_state = new_state
            i+=1
        new_lines.append(line)
    f = open(filepath, 'w')
    f.writelines(new_lines)


def go_from_plus(x):
    return go_from_plus_or_minus('+', x)

def go_from_minus(x):
    return go_from_plus_or_minus('-', x)

def go_from_plus_or_minus(op, x):
    if x == op:
        return 10
    elif x == '=':
        return 2
    else:
        return 9

def get_new_state_decider(x):
    return {
        0: go_from_zero_state,
        1: go_from_plus,
        3: go_from_minus,
        4: lambda x: 2 if x == '>' or x == '=' else 9,
        5: lambda x: 2 if x == '<' or x == '=' else 9,
        6: lambda x: 2 if x == '&' or x == '=' else 9,
        7: lambda x: 2 if x == '|' or x == '=' else 9,
        8: lambda x: 2 if x == '=' else 9,
    }.get(x, lambda x: 0)


def go_from_zero_state(x):
    if x == '+':
        return 1
    elif x == '-':
        return 3
    elif x == '>':
        return 4
    elif x == '<':
        return 5
    elif x == '&':
        return 6
    elif x == '|':
        return 7
    elif x == '%' or x == '^' or x == '*' or x == '/' or x == '=':
        return 8
    else:
        return 0



