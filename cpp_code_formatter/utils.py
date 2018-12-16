def get_state(prev_state):
    return {
        0: choose_from_states,
        1: choose_from_states,
        2: lambda x: 3 if x == '/' or x == '*' else 4,
    }.get(prev_state, 4)

def choose_from_states(x):
    if x == '\n' or x == '\t' or x == ' ' or x == ';' or x == ',':
        return 1
    elif x == '/':
        return 2
    else:
        return 4

def only_spaces_and_special_characters(line):
    prev_state = 0
    for symbol in line:
        prev_state = (get_state(prev_state))(symbol)
        if prev_state == 3:
            return True
        elif prev_state == 4:
            return False
    if prev_state == 1 or prev_state == 3 or prev_state == 0:
        return True
    return False


def line_beggining_spaces_edit(indentation, spaces, nesting, line):
    needed_spaces = indentation * nesting - spaces
    if needed_spaces >= 0:
        return ' ' * needed_spaces + line
    else:
        return line[-needed_spaces:]


def get_side_spaces(line, left_space, right_space):
    left = ""
    right = ""
    if left_space >= 0 and line[left_space] != ' ':
        left = " "
    if right_space < len(line) and line[right_space] != ' ':
        right = " "
    return left, right


def delete_left_right(line, left_space, right_space):
    right = right_space
    left = left_space
    while left >= 0 and left_space < len(line) and line[left] == ' ':
        left-=1
    while right < len(line) and line[right] == ' ':
        right+=1

    if left < 0: left = 0
    if right >= len(line): right = len(line) - 1
    line = line[:left + 1] + line[left_space + 1 : right_space] + line[right:]
    return line, (left_space - left) + (right - right_space)

def indentation_message(needed_spaces, line_num):
    if needed_spaces > 0:
        print("Add", needed_spaces, "spaces to line number ", line_num)
    elif needed_spaces < 0:
        print("Delete", -needed_spaces, "spaces from line number ", line_num)

def only_spaces_and_newlines(line):
    for symbol in line:
        if symbol != ' ' and symbol != '\n':
            return False
