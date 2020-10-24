import textwrap
import sys
import time
from termcolor import colored, cprint


def draw_welcome_screen():

    print("")
    cprint(f'    Varmt välkomna till PokéMood!', 'cyan')
    cprint(f'    Ett textbaserat spel med humörstyrda Poketerer!', 'cyan')
    cprint(f'    Med hjälp av twitter kommer du få en chans att \n    påverka din Poketers pokemör!', 'cyan')
    cprint(f'    Men passa dig, är du fel ute kan det också bli minus!.\n', 'cyan')

    cprint(colored("""    ⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿Pik'a'mood-⣿⣿⣿⣿⣿⣿⣿⡿⣿
    ⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿-trollet⣿⣿⠿⠛⠉⠁⠀⢸
    ⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
    ⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿""", "yellow"))
    cprint(f'    Nu kör vi!! \n', 'yellow')


def delay_print(intro_text, s, a):
    print(intro_text)
    for i in s:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)
    print(a)
    time.sleep(0.5)


def atk_txt(attacker, reciver, text):
    print(f"{attacker} attackerar {reciver} ")
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)
    print('''
          |
O=========|>>>>>>>>>>>>>>>>>>>>>>>>>>
          |
    ''')
    time.sleep(0.5)


def successful_block(blocker):
    print(f"{blocker} försöker blockera")
    text = "Lyckad block!"
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    print('''
      |`-._/\_.-`|
      |    ||    |
      |___o()o___|
      |__((<>))__|
      \   o\/o   /
       \   ||   /
        \  ||  /
         '.||.'
    ''')


def unsuccessful_block(blocker):
    print(f"{blocker} försöker blockera")
    text = "Misslyckad block!"
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.1)
    print('''
      |`-._/<    <\_.-`|
      |    |>    >|    |
      |___o(<    <)o___|
      |__((<>    >>))__|
      \   o\>   > /o   /
       \   |<    <|   /
        \  |>    <|  /
          '.|>   <|.'
    ''')


def print_frame(rows, table_color, indentation):
    print(colored("""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *"""
        , table_color))

    line_width = 85
    for row in rows:
        dedented_row = textwrap.dedent(row).strip()
        chopped_lines = textwrap.fill(dedented_row, line_width)
        print(textwrap.indent(chopped_lines, ' ' * indentation))

    print(colored(
        """        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------"""
    , table_color))

