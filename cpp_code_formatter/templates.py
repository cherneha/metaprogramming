from pathlib import Path

class FormatTemplate():
    def __init__(self, name, indentation, operator_spaces, lines_between_blocks):
        self.name = name
        self.indentation = indentation
        self.operator_spaces = operator_spaces
        self.lines_between_blocks = lines_between_blocks


def load_all_templates(filepath):
    if not Path(filepath).is_file():
        file = open(filepath, mode='w+')
        file.write("standard 4 True 2\n")
        file.close()
    file = open(filepath, mode='r')
    lines = file.readlines()
    file.close()
    return lines


def append_to_file(filepath, line):
    file = open(filepath, mode='a')
    file.write(line)
    file.close()

def get_template_params(filepath, template_name):
    lines = load_all_templates(filepath)
    for line in lines:
        params = line.split(" ")
        if params[0] == template_name:
            if len(params) == 4:
                return FormatTemplate(template_name, int(params[1]), bool(params[2]), int(params[3]))
    print("Such template does not exist.")
    return None

def list_templates(filepath):
    lines = load_all_templates(filepath)
    if lines is not None:
        for line in lines:
            params = line.split(" ")
            print(params[0] + ": " + "indentation = " + params[1] + ", operator spaces = " + params[2]
                  + ", lines between main code blocks = ", params[3])
    return None

def save_template(filepath, format_template):
    lines = load_all_templates(filepath)
    for line in lines:
        params = line.split(" ")
        if params[0] == format_template.name:
            print("Such template name already exists.")
            return False
    insertion_line  = format_template.name + " " + str(format_template.indentation) + \
                      " "  + str(format_template.operator_spaces) + " " + str(format_template.lines_between_blocks) + '\n'
    append_to_file(filepath, insertion_line)
    return True








