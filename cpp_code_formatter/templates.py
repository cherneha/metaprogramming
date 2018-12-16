class FormatTemplate():
    def __init__(self, name, indentation, operator_spaces, lines_between_blocks):
        self.name = name
        self.indentation = indentation
        self.operator_spaces = operator_spaces
        self.lines_between_blocks = lines_between_blocks


def load_all_templates(filepath):
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
                return FormatTemplate(template_name, params[1], params[2], params[3])

def list_templates(filepath):
    lines = load_all_templates(filepath)
    for line in lines:
        params = line.split(" ")
        print(params[0] + ": ", + "indentation = " + params[1] + ", operator spaces = " + params[2]
              + ", lines between main code blocks = ", params[3])

def save_template(filepath, format_template):
    lines = load_all_templates(filepath)
    for line in lines:
        params = line.split(" ")
        if params[0] == format_template.name:
            print("Such template name already exists.")
            return False
    insertion_line  = format_template.name + " " + format_template.indentation + \
                      " "  + format_template.operator_spaces + " " + format_template.lines_between_blocks
    append_to_file(filepath, insertion_line)
    return True








