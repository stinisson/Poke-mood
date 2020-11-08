import random
import textwrap

from colorama import init
from termcolor import cprint

from Textbased_Pygame.cards_helper import get_cities, choose_city
from Textbased_Pygame.mood_score import calc_mood_score
from Textbased_Pygame.print_module import print_frame
from poketer import *

init()


class User:
    def __init__(self, name):
        self.name = name
        self.team = []

    def add_team(self, poketer):
        self.team.append(poketer)

    def __repr__(self):
        return f'Namn: {self.name}, Team: {self.team}'


def draw_welcome_screen():
    print("")
    cprint(f'    Welcome to PookéMood!', 'cyan')
    cprint(f'    Use your Pokeéter to defeat your opponent! !', 'cyan')
    cprint(f'    Your Pokeéter has its own mood. By using Twitter\n    you are able to incresse the health and \n'
           f'    power of your Pokeéter.', 'cyan')

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
    cprint(f'    Let us begin!! \n', 'yellow')


def poketer_mood_explanation_text(username):
    row1 = f"Hello {username}!"
    row2 = f"""All Pokeéters has its own mood. These moods can be either  {colored('Happy', 'yellow')} or {colored('Angry', 'red')}."""
    row3 = f"{colored('Happy Pokeéter preform best in surroundings with happy shouts, laughter and a cheerful atmosphere. Life is a party!', 'yellow')}"
    row4 = f"{colored('Angry Pokeéter grow in strength under controversy and hostile conditions. Shoot, dig, shut up!', 'red')}"

    print_frame_with_newline([row1, row2, row3, row4], 'white', 15)


def print_frame_with_newline(rows, table_color, indentation):
    print(colored("""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *"""
                  , table_color))

    line_width = 85
    for row in rows:
        chopped_lines = textwrap.fill(row, line_width)
        print(textwrap.indent(chopped_lines, ' ' * indentation))
        print("")

    print(colored(
        """        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------"""
        , table_color))


def intro_card(poketer, is_cpu, live):
    if is_cpu:
        cities = get_cities()
        city = random.choice(cities)
    else:
        x = """

        Your Pokeéter has a certain mood. You now have the opportunity to increase your Pokeéter's health
        by searching for a city in Sweden where you think the inhabitants are in the same mood as your Pokeéter.
        The residents' mood is based on what they tweet. The more emotional they are, the more they increase
        your Pokeéter's health. Good luck!

        """
        print_frame([x], 'white', 15)
        city = choose_city()

    print("This may take a while. Hang on! :)")

    mood_score = calc_mood_score(poketer.mood, city, live=live)

    if mood_score is None:
        poketer.add_health(20)
        poketer.add_max_health(20)
    else:
        poketer.add_health(mood_score)
        poketer.add_max_health(mood_score)

    if is_cpu:
        w = f"{poketer.name} selected {city.capitalize()}. Tweet, tweet!"
    else:
        w = f"... Tweet, tweet! Calculates mood for the inhabitants of {city.capitalize()} ..."

    x = f"{poketer.name} increased its health by {mood_score} p! {poketer.catchword}"
    if mood_score is None:
        x = f"Something went wrong but {poketer.name} increased its health by 20 p! {poketer.catchword}"

    y = ""
    z = poketer.get_stats()
    print_frame([w, x, y, z], poketer.color, 15)

    input("\nPress Enter to continue")


def start_game(live):
    draw_welcome_screen()
    username = input("Please enter your name: ")
    poketer_mood_explanation_text(username)
    input("\nPress Enter to continue\n")

    gunnar = Poketer(colored("Happy Gunnar", 'yellow'), 'happy', 'yellow', 50, 50, 45, catchword="#YOLO")
    ada = Poketer(colored("Aggressiva Ada", 'red'), 'angry', 'red', 50, 50, 45, catchword="#FTW")
    #louise = Poketer(colored("Ledsna Louise", 'blue'), 'sad', 'blue', 50, 50, 45, catchword="#TGIF")
    #kalle = Poketer(colored("Kärleksfulla Kalle", 'magenta'), 'loving', 'magenta', 50, 50, 45, catchword="#XOXO")


    user = User(colored(username, gunnar.color))
    user.add_team(gunnar)

    cpu = User(colored("Olof", ada.color))
    cpu.add_team(ada)

    x = f"\n{user.name}, your Pokeéter is {gunnar.name}."
    y = gunnar.get_stats()
    print_frame([x, y], gunnar.color, 15)

    x = f"Your opponent is {cpu.name}. {cpu.name} has choosen Pokeéter {ada.name}. {ada.get_stats()}"
    print_frame([x], ada.color, 15)

    input("\nPress Enter to continue")
    intro_card(poketer=gunnar, is_cpu=False, live=live)
    intro_card(poketer=ada, is_cpu=True, live=live)


if __name__ == '__main__':
    start_game(live=False)
