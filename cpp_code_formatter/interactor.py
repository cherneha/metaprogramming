from formatter import edit_dir_files
from templates import FormatTemplate, save_template
import os

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
                project = input("give me your shitty project dir address")
                edit_dir_files('/home/stacy/CODE/metaprogramming/EDITOR-master', 4, False, False)
            elif choise == 2:
                print("let's see if it's even possible")
                project = input("give me your shitty project dir address")
                edit_dir_files('/home/stacy/CODE/metaprogramming/EDITOR-master', 4, False, True)
            elif choise == 3:
                template_creation()
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
    lines_between_main_blocks = int(input("How many lines between main blocks of code?"))
    template_name = str(input("ok, now give this template a name"))
    format_template = FormatTemplate(template_name, indentation, del_operator_spaces, lines_between_main_blocks)
    save_template(format_template)
    print()
    # edit_dir_files('/home/stacy/CODE/metaprogramming/EDITOR-master', indentation, del_operator_spaces, True)

