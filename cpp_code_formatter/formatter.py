import glob
from utils import only_spaces_and_special_characters, line_beggining_spaces_edit, get_side_spaces, delete_left_right, indentation_message, only_spaces_and_newlines


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
    new_lines_between_blocks(filepath, 3)


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
                    code = [ending] + code
                    new_line = new_line[:(n + 1)] + '\n'
                break
            elif symbol == '}':
                nesting -= 1
                n = line.find('}')
                ending = line[n + 1:]
                new_line = line_beggining_spaces_edit(indentation, spaces, nesting, line)
                if not only_spaces_and_special_characters(ending):
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


def new_lines_between_blocks(filepath, n):
    file = open(filepath, mode='r')
    code = file.readlines()
    nesting = 0
    file.close()
    file = open(filepath, mode='w')
    new_lines = []

    i = 0
    while i < len(code):
        line = code[i]
        new_lines.append(line)
        for symbol in line:
            if symbol == '{':
                nesting += 1
                break
            elif symbol == '}':
                nesting -= 1
                if nesting == 0:
                    free_lines = 0
                    j = i + 1
                    while j < len(code) and only_spaces_and_newlines(code[j]):
                        free_lines += 1
                        j += 1
                    free_lines_diff = n - free_lines
                    if free_lines_diff < 0:
                        i -= free_lines_diff
                    else:
                        while free_lines_diff > 0:
                            free_lines_diff -= 1
                            new_lines.append('\n')
                break

        i += 1

    file.writelines(new_lines)


def go_from_plus(x):
    return go_from_plus_or_minus('+', x)

def go_from_minus(x):
    res = go_from_plus_or_minus('-', x)
    if res == 9 and x == '>': return 10
    else: return res

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



