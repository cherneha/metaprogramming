from formatter import edit_dir_files, analyze_dir_files
from templates import FormatTemplate, save_template, list_templates, get_template_params
import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, 'templates.txt')

def run_formatter():
    repeat = 'yes'
    while (repeat == 'yes' or repeat == 'Yes' or repeat == 'YES' or repeat == 'y'
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
                project = get_path_from_user()
                indentation = int(input("number of spaces for indentation: "))
                analyze_dir_files(project, FormatTemplate("analyze temp", indentation, True, 2))
            elif choise == 2:
                print("let's see if it's even possible")
                format_template = FormatTemplate("standard", 4, True, 2)
                template_correct = False
                while not template_correct:
                    print("Available templates:")
                    list_templates(TEMPLATE_PATH)
                    template_name = str(input("which template? (hit Enter if standard)"))
                    if template_name == "":
                        template_correct = True
                    else:
                        format_template = get_template_params(TEMPLATE_PATH, template_name)
                        if format_template is not None:
                            template_correct = True

                project = get_path_from_user()
                edit_dir_files(project, format_template)
            elif choise == 3:
                template_creation(TEMPLATE_PATH)
            else:
                print("well, u can't even pick an option normally")
                choise = 0

        repeat = input("Repeat?")


def template_creation(filepath):
    print("u think u can make a normal template??")
    indentation = int(input("number of spaces for indentation: "))
    answer = ''
    while answer != 'a' and answer != 'd':
        answer = input("Add or delete spaces around operators? (a/d)")
    if answer == 'a':
        del_operator_spaces = False
    else:
        del_operator_spaces = True
    norm_input = False
    while not norm_input:
        lines_between_main_blocks = input("How many lines between main blocks of code?")
        try:
            lines_between_main_blocks = int(lines_between_main_blocks)
            norm_input = True
        except Exception:
            pass

    success = False
    while not success:
        template_name = str(input("ok, now give this template a name"))
        format_template = FormatTemplate(template_name, indentation, del_operator_spaces, lines_between_main_blocks)
        success = save_template(filepath, format_template)
        if not success:
            print("ok. let's try again...")
    print("Template created and saved.")
    # edit_dir_files('/home/stacy/CODE/metaprogramming/EDITOR-master', indentation, del_operator_spaces, True)


def get_path_from_user():
    folder_correct = False
    project = str()
    while not folder_correct:
        project = str(input("give me your shitty project dir address"))
        project_path = Path(project)
        folder_correct = project_path.is_dir()
    return project