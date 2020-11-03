import textwrap
import sys
import time
from termcolor import colored, cprint
from colorama import init
import warnings
import random
from Textbased_Pygame.cards_helper import get_cities, choose_city, get_emotions, choose_emotion, take_integer_input
from pokemood_text_based.common import choose_poketer
from pokemood_text_based.mood_analysis import mood_analysis
from Textbased_Pygame.mood_score import calc_mood_score
from Textbased_Pygame.print_module import print_frame
from pokemood_text_based.quiz import quiz
from pokemood_text_based.sentiment_analysis import sentiment_analysis
from pygame_states import gunnar, ada
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
    cprint(f'    Varmt välkomna till PokéMood!', 'cyan')
    cprint(f'    Ett textbaserat spel med humörstyrda Poketerer!', 'cyan')
    cprint(f'    Med hjälp av Twitter kommer du få en chans att \n    påverka din Poketers pokemör!', 'cyan')
    cprint(f'    Men passa dig, är du fel ute kan det också bli minus!\n', 'cyan')

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


def poketer_mood_explanation_text(username):
    row1 = f"Hej {username}!"
    row2 = f"""Alla Poketerer har ett visst grundhumör. De kan vara {colored('glada', 'yellow')}, {colored('arga', 'red')}, {colored('ledsna', 'blue')} eller {colored('kärleksfulla', 'magenta')}."""
    row3 = f"{colored('Glada Poketerer trivs bäst i omgivningar med glada tillrop, skratt och uppsluppen stämning. Livet är en fest!', 'yellow')}"
    row4 = f"{colored('Arga Poketerer växer i styrka under kontroverser och fientliga förhållanden. Skjut, gräv, tig!', 'red')}"
    row5 = f"{colored('Ledsna Poketerer mår som bäst omgivna av nedstämdhet, sorg och ledsamheter. Saliga äro de som sörja!', 'blue')}"
    row6 = f"{colored('Kärleksfulla Poketerer frodas i miljöer med mycket värme, kramar och omtänksamhet. Man kan aldrig få för många kramar!', 'magenta')}"
    print_frame_with_newline([row1, row2, row3, row4, row5, row6], 'white', 15)


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

        Your Poketer has a certain mood. You now have the opportunity to increase your Poketer's health
        by searching for a city in Sweden where you think the inhabitants are in the same mood as your Poketer.
        The residents' mood is based on what they tweet. The more emotional they are, the more they increase
        your Poketer's health. Good luck!

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
    username = input("Vänligen ange ditt namn: ")
    poketer_mood_explanation_text(username)
    input("\nTryck enter för att fortsätta\n")

    gunnar = Poketer(colored("Glada Gunnar", 'yellow'), 'happy', 'yellow', 50, 50, 45, catchword="#YOLO")
    ada = Poketer(colored("Aggressiva Ada", 'red'), 'angry', 'red', 50, 50, 45, catchword="#FTW")
    #louise = Poketer(colored("Ledsna Louise", 'blue'), 'sad', 'blue', 50, 50, 45, catchword="#TGIF")
    #kalle = Poketer(colored("Kärleksfulla Kalle", 'magenta'), 'loving', 'magenta', 50, 50, 45, catchword="#XOXO")


    user = User(colored(username, gunnar.color))
    user.add_team(gunnar)

    cpu = User(colored("Olof", ada.color))
    cpu.add_team(ada)

    x = f"\n{user.name}, din Poketer är {gunnar.name}."
    y = gunnar.get_stats()
    print_frame([x, y], gunnar.color, 15)

    x = f"Din motståndare är {cpu.name}. {cpu.name} valde poketer {ada.name}. {ada.get_stats()}"
    print_frame([x], ada.color, 15)

    input("\nTryck enter för att fortsätta")
    intro_card(poketer=gunnar, is_cpu=False, live=live)
    intro_card(poketer=ada, is_cpu=True, live=live)


if __name__ == '__main__':
    start_game(live=False)
