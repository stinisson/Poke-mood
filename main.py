"""Pokemon Battle GO!"""
from twitter_search import geocodes
from mood_score import calc_mood_score
from mood_analysis import mood_analysis, text_emotions
from sentiment_analysis import sentiment_analysis

from mood_score import calc_mood_score
import sys
from random import randint
import random
import time
from termcolor import colored, cprint
import colorama

colorama.init()
from prints_module import delay_print, atk_txt, successful_block, unsuccessful_block


# TODO:
# 1- Rad printen på rad 24 bör ligga och fånga stadsinput som en else på rad 112 t.ex


class Poketer:
    def __init__(self, name, mood, health, max_health, attack):
        self.name = name
        self.mood = mood
        self.health = health
        self.max_health = max_health
        self.attack = attack

    def attack_fnc(self, opponent_pokemon):
        opponent_pokemon.health -= self.attack
        atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
        self.healtcheck_color(opponent_pokemon)

    def healtcheck_color(self, opponent_pokemon):

        if opponent_pokemon.health >= opponent_pokemon.max_health / 2:
            print(f"{opponent_pokemon.name} hälsa: {colored(opponent_pokemon.health, 'green')}\n")
        elif opponent_pokemon.max_health / 4 <= opponent_pokemon.health <= opponent_pokemon.max_health / 2:
            print(f"{opponent_pokemon.name} hälsa: {colored(opponent_pokemon.health, 'yellow')}\n")
        elif opponent_pokemon.health <= opponent_pokemon.max_health / 4:
            print(f"{opponent_pokemon.name} hälsa: {colored(opponent_pokemon.health, 'red')}\n")

    def healthcheck(self,opponent_pokemon, opponent_name):
        if self.health <= 0 or opponent_pokemon.health <= 0:
            if opponent_pokemon.health <= 0:
                print(f'*** {opponent_name} Poketer {opponent_pokemon} svimmade. Du vann! ***')
            if self.health <= 0:
                print(f'*** Din poketer {self.name} svimmade. {opponent_name} vann! ***')
            alive = False
            return alive

    def block(self, opponent, opponent_pokemon):
        block_chance = randint(1, 11)
        if block_chance <= 7:
            time.sleep(1)
            self.health -= opponent_pokemon.attack // 2
            delay_print(f"{opponent.name} attackerar {self.name}", "3 2 1...", "Boom!") # Ändrade så att det stod "attackerar" som de andra printsatserna
            successful_block(self.name) # Flyttade ner denna så att den hamnar efter attacken, ser bättre ut
            print(f"{self.name} tog {opponent_pokemon.attack // 2} i skada!\n")

        elif block_chance >= 8:
            time.sleep(1)
            self.health -= opponent_pokemon.attack
            delay_print(f"{opponent.name} attackerar med {opponent_pokemon.name}", "3 2 1...", "Boom!")
            unsuccessful_block(self.name)
            print(f"{self.name} tog {opponent_pokemon.attack} i skada!\n")

    def update_max_health_by_city_mood(self, city, user_name):
        mood_score = calc_mood_score(self.mood, city, live=False)

        if mood_score == None:
            #print("Tyvärr något gick fel, men du får 20 extra i hälsa. ")
            self.max_health += 20
            self.health += 20
            return 20
        else:
            self.health += mood_score
            self.max_health += mood_score
            #print(f"{user_name} valde {city} med mycket {self.mood}-content!")
            #print(
            #    f"Hälsan för {self.name} ökade med {mood_score}. Total hälsa: {colored(self.max_health, 'green')}\n")

        return mood_score
    def __repr__(self):
        return f'Poketer: {self.name} Mood: {self.mood}'


class User:
    def __init__(self, name):
        self.name = name
        self.team = []

    def add_team(self, poketer):
        self.team.append(poketer)

    def __repr__(self):
        return f'Namn: {self.name}, Team: {self.team}'


def main():
    user_pokemon = Poketer(colored("Happy Hasse", 'blue'), "happy", 10, 10, 5)
    cpu_pokemon = Poketer(colored("Aggressive Ada", 'red'), "angry", 10, 10, 5)

    cprint(f'    Varmt välkomna till PokéMood!', 'cyan')

    cprint(colored("""⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
    ⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿
    ⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
    ⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿\n""", "yellow"))

    username = input("Vänligen ange ditt namn: ")
    user = User(colored(username, 'blue'))
    cpu = User(colored("Olof", 'red'))
    user.add_team(user_pokemon)
    cpu.add_team(cpu_pokemon)
    print(f"Hej {user.name}. Din poketer är {user_pokemon.name}.")
    print(f"Din motståndare är {cpu.name} och har valt poketer {cpu_pokemon.name}.\n")
    print(f"{user.name}, det är din tur! ")

    # print(f"Välj en stad du tror att det är mycket {user_pokemon.mood} content i.")
    # city = input("Välj mellan Göteborg eller Stockholm: ")
    # delay_print("Beräknar mood'content", ".....", "")
    #

    """ A """

    x = """Din Pokemon har ett visst humör. Du har nu möjligheten att öka din pokemons hälsa genom
            att söka efter en stad i Sverige där du tror att invånarna är på samma humör som din pokemon.
            Invånarnas humör baseras på vad de twittrar. Ju mer känslosamma de är desto mer ökar 
            din Pokemons hälsa. Lycka till!"""
    print(f"""\n
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *
            {x}                                         
        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        """)


    for idx, city in enumerate(geocodes):
        if city:
            print(idx + 1, city.capitalize())
    city_choice = int(input(f"Vilken stad väljer du? (1-{len(geocodes) - 1}): "))
    city_list = list(geocodes)
    city = city_list[city_choice - 1]

    mood_score = user_pokemon.update_max_health_by_city_mood(city, user.name)

    x = f" ... Beräknar humör för invånarna i {city.capitalize()} ..."
    y = f"{user_pokemon.name} fick {mood_score} i ökad hälsa! #YOLO"
    if not mood_score:
        y = f"Något gick fel men {user_pokemon.name} får 20 p i ökad hälsa! #YOLO"

    print(f"""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *
                         {x}
                         {y}
        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        """)

    cpu_city_choice = random.choice(city_list)
    mood_score = cpu_pokemon.update_max_health_by_city_mood(cpu_city_choice, cpu.name)
    x = f"{cpu.name} valde {cpu_city_choice.capitalize()}"
    y = f"{cpu_pokemon.name} fick {mood_score} i ökad hälsa! #FTW"

    print(f"""\n
        ****************************************************************************************************
        ^                                                                                                  ^
                         {x}
                         {y}
        ^                                                                                                  ^
        ****************************************************************************************************
        """)

    input("Tryck enter för att fortsätta")


    # if city == "Göteborg":
    #     user_pokemon.update_max_health_by_city_mood("Göteborg", user.name)
    #     cpu_pokemon.update_max_health_by_city_mood("Stockholm", cpu.name)
    #
    # elif city == "Stockholm":
    #     user_pokemon.update_max_health_by_city_mood("Stockholm", user.name)
    #     cpu_pokemon.update_max_health_by_city_mood("Göteborg", cpu.name)
    #
    # else:
    #     print("Tyvärr denna staden är ej tillgänglig, men du får 20 extra i hälsa. ")
    #     user_pokemon.max_health += 20
    #     user_pokemon.health += 20
    #     print(
    #         f"Hälsan för {user_pokemon.name} ökade med 20. Total hälsa: {colored(user_pokemon.max_health, 'green')}\n")
    #     cpu_pokemon.update_max_health_by_city_mood("Stockholm", cpu.name)

    """ B """

    x = """ Attack-bonus! Du har nu chansen att öka din pokemons attack-styrka. 
             Välj en stad och gissa vilket humör som är mest förekommande 
             bland invånarna. Lycka till! """
    print(f"""\n
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *
            {x}                                         
        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        """)

    for idx, city in enumerate(geocodes):
        if city:
            print(idx + 1, city.capitalize())
    city_choice = int(input(f"Vilken stad väljer du? (1-{len(geocodes) - 1}): "))
    city_list = list(geocodes)
    city = city_list[city_choice - 1]

    for idx, emotion in enumerate(text_emotions):
        print(idx + 1, emotion.capitalize())
    emotion_choice = int(input(f"Vilken känsla är mest förekommande i {city.capitalize()}? (1-{len(text_emotions)}): "))
    emotion_list = list(text_emotions)
    emotion = emotion_list[emotion_choice - 1]

    most_frequent_emotions = mood_analysis(city=city, live=False)

    attack_bonus = 10
    if emotion in most_frequent_emotions:
        user_pokemon.attack += attack_bonus
        x = f"""Rätt! Vanligast är att man är {emotion} i {city.capitalize()}.
                         Din pokemon belönas med {attack_bonus} p i ökad attack-styrka!"""
    else:
        x = f"""Tyvärr! I {city.capitalize()} är man {most_frequent_emotions[0]}, inte {emotion}!
                         Du får ingen attack-bonus."""

    print(f"""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *
                         {x}
        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        """)

    x = f"{cpu.name} valde Kiruna och gissade 'kärleksfull', vilket var rätt!"
    y = f"{cpu_pokemon.name} får {attack_bonus} p i ökad attack-styrka! #FTW"

    print(f"""\n
        ****************************************************************************************************
        ^                                                                                                  ^
                         {x}
                         {y}
        ^                                                                                                  ^
        ****************************************************************************************************
        """)

    input("Tryck enter för att fortsätta")

    """ C """

    x = """    Twitter-vadslagning! Har du koll på vad som trendar på sociala medier? 
                Skriv in ett ord och på vilket språk du vill använda i sökningen. Gissa om 
                de senaste tweetsen som innehåller detta ord är mest positiva, mest negativa
                eller neutrala. Om du gissar rätt belönas du med 20 p i ökad hälsa.
                Om du gissar fel bestraffas du med 20 p minskad hälsa. Lycka till! """

    print(f"""\n
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *
            {x}                                         
        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        """)

    print("Skriv in ett nyckelord att söka efter på Twitter. Exempel: COVID, Donald Trump, Estonia.")
    keyword_choice = input(">> ")

    language_choice = input("Vilket språk vill du söka efter? [S]venska eller [E]ngelska? ")
    if language_choice.lower() == "s":
        language_choice = "swedish"
    elif language_choice.lower() == "e":
        language_choice = "english"

    print(f"Tror du folket på Twitter är mest positivt, mest negativt eller neutralt inställda till {keyword_choice}? ")
    attitude_choice = input("[P]ostiva - [N]egativa - ne[U]trala? ")
    if attitude_choice.lower() == "p":
        attitude_choice = "positivt"
    elif attitude_choice.lower() == "n":
        attitude_choice = "negativt"
    elif attitude_choice.lower() == "u":
        attitude_choice = "neutralt"

    print("Det här kan ta en liten stund... Vänligen vänta. :)")

    # Ni får testköra genom att söka efter covid på engelska
    result = sentiment_analysis(keyword=keyword_choice, language=language_choice,
                                file_name='demo_tweets_english_covid.p', live=False)

    health_bonus = 10
    if attitude_choice == result:
        user_pokemon.health += health_bonus
        user_pokemon.max_health += health_bonus
        x = f"""Rätt! {keyword_choice} har mest {result} innehåll på Twitter.
                         Din pokemon belönas med {health_bonus} poäng i ökad hälsa!"""
    else:
        user_pokemon.health -= health_bonus
        user_pokemon.max_health -= health_bonus
        x = f"""Tyvärr, {keyword_choice} har mest {result} innehåll på Twitter!
                         Din pokemon bestraffas med {health_bonus} p i minskad hälsa."""

    print(f"""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *
                         {x}
        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        """)

    input("Tryck enter för att fortsätta")

    x = "Nu är det dags för battle!"

    print(f"""
        ----------------------------------------------------------------------------------------------------
        *                                                                                                  *
                         {x}
        *                                                                                                  *
        ----------------------------------------------------------------------------------------------------
        """)

    input("Tryck enter för att fortsätta")

    #print("*** Dags för battle! ***\n")

    while (user_pokemon.health >= 0) and (cpu_pokemon.health >= 0):
        if user_pokemon.health <= 0 or cpu_pokemon.health <= 0:
            if cpu_pokemon.health <= 0:
                break
            if user_pokemon.health <= 0:
                print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu.name} vann! ***')
                break

        else:
            print(f"*** Det är {colored('din', 'blue')} tur ***")
            user_choose = int(input("Vill du [1] attackera eller [2] blockera? "))
            if user_choose == 1:
                user_pokemon.attack_fnc(cpu_pokemon)
                if user_pokemon.healthcheck(cpu_pokemon, cpu.name) is False:
                    break

            elif user_choose == 2:
                user_pokemon.block(cpu, cpu_pokemon)
                if user_pokemon.healthcheck(cpu_pokemon, cpu.name) is False:
                    break

            if cpu_pokemon.health > 0:
                print(f'*** Det är {cpu.name} tur ***')
                cpu_pokemon.attack_fnc(user_pokemon)
                if user_pokemon.healthcheck(cpu_pokemon, cpu.name) is False:
                    break



if __name__ == '__main__':
    main()
