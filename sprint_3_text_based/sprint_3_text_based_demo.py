"""Pokemon Battle GO!"""
from twitter_search import geocodes
from mood_score import calc_mood_score
from mood_analysis import mood_analysis, text_emotions
from sentiment_analysis import sentiment_analysis
from random import randint
import random
import time
from termcolor import colored, cprint
import colorama
import sys

colorama.init()
from print_module import delay_print, atk_txt, successful_block, unsuccessful_block, print_frame, draw_welcome_screen, \
    print_frame_with_newline, poketer_mood_explanation_text, draw_end_screen


class User:
    def __init__(self, name):
        self.name = name
        self.team = []

    def add_team(self, poketer):
        self.team.append(poketer)

    def __repr__(self):
        return f'Namn: {self.name}, Team: {self.team}'


class Poketer:
    def __init__(self, name, mood, color, health, max_health, attack, catchword):
        self.name = name
        self.mood = mood
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.color = color
        self.catchword = catchword

    def attack_fnc(self, opponent_pokemon, opponent):
        miss_chance = randint(1, 6)
        crit_chance = randint(1, 6)
        dmg_modifier = randint(-3, 3)
        if miss_chance <= 5:
            if crit_chance >= 5:
                opponent_pokemon.health -= (self.attack + dmg_modifier) * 2
                atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
                print("Dubbel skada!")
                self.healtcheck_color(opponent_pokemon)
                # self.healthcheck(opponent_pokemon, opponent.name)
            else:
                opponent_pokemon.health -= (self.attack + dmg_modifier)
                atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
                self.healtcheck_color(opponent_pokemon)
                # self.healthcheck(opponent_pokemon, opponent.name)
        else:
            print("Attacken missade...")

        # opponent_pokemon.health -= self.attack
        # atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
        # self.healtcheck_color(opponent_pokemon)

    def healtcheck_color(self, opponent_pokemon):

        if opponent_pokemon.health >= opponent_pokemon.max_health / 2:
            print(f"{opponent_pokemon.name} hälsa: {colored(opponent_pokemon.health, 'green')}\n")
        elif opponent_pokemon.max_health / 4 <= opponent_pokemon.health <= opponent_pokemon.max_health / 2:
            print(f"{opponent_pokemon.name} hälsa: {colored(opponent_pokemon.health, 'yellow')}\n")
        elif opponent_pokemon.health <= opponent_pokemon.max_health / 4:
            print(f"{opponent_pokemon.name} hälsa: {colored(opponent_pokemon.health, 'red')}\n")

    def healthcheck(self, opponent_pokemon, opponent_name):
        if self.health <= 0 or opponent_pokemon.health <= 0:
            if opponent_pokemon.health <= 0:
                print(f'*** {opponent_name} Poketer {opponent_pokemon.name} svimmade. Du vann! ***')
            if self.health <= 0:
                print(f'*** Din poketer {self.name} svimmade. {opponent_name} vann! ***')
            alive = False
            return alive

    def block(self, opponent, opponent_pokemon):
        block_chance = randint(1, 11)
        if block_chance <= 7:
            time.sleep(1)
            self.health -= opponent_pokemon.attack // 2
            delay_print(f"{opponent.name} attackerar {self.name}", "3 2 1...",
                        "Boom!")  # Ändrade så att det stod "attackerar" som de andra printsatserna
            successful_block(self.name)  # Flyttade ner denna så att den hamnar efter attacken, ser bättre ut
            print(f"{self.name} tog {opponent_pokemon.attack // 2} i skada!\n")

        elif block_chance >= 8:
            time.sleep(1)
            self.health -= opponent_pokemon.attack
            delay_print(f"{opponent.name} attackerar med {opponent_pokemon.name}", "3 2 1...", "Boom!")
            unsuccessful_block(self.name)
            print(f"{self.name} tog {opponent_pokemon.attack} i skada!\n")

    def attack_bonus(self, city, emotion, emotions, attack_bonus):
        if emotion in emotions:
            self.attack += attack_bonus
            w = f"""Det var rätt! I {city.capitalize()} är man {emotion}."""
            x = f"""{self.name} får {attack_bonus} p i ökad attack-styrka!"""
        else:
            self.attack -= attack_bonus
            w = f"Tyvärr! I {city.capitalize()} är man {emotions[0]}, inte {emotion}!"
            x = f"{self.name} bestraffas med {attack_bonus} p i minskad attack-styrka."
        y = ""
        z = self.get_stats()

        print_frame([w, x, y, z], self.color, 15)

    def health_bonus(self, result, keyword, attitude):
        while True:
            if result == 'connection_error':
                x = f"Det går tyvärr inte att söka på Twitter just nu. Försök igen senare!"
                print_frame([x], 'white', 15)
                break

            if result == 'too_few_results':
                x = f"""Hittade för få tweets innehållandes {keyword}.
        Ett tips är att söka efter något som är mer aktuellt i samhällsdebatten."""
                print_frame([x], 'white', 15)
            else:
                break

        health_bonus = 10
        if result != 'connection_error':
            if attitude == result:
                self.health += health_bonus
                self.max_health += health_bonus
                w = f"Rätt! {keyword} har mest {result} innehåll på Twitter."
                x = f"{self.name} belönas med {health_bonus} p i ökad hälsa!"
            else:
                self.health -= health_bonus
                self.max_health -= health_bonus
                w = f"""Tyvärr, {keyword} har mest {result} innehåll på Twitter!"""
                x = f"""{self.name} bestraffas med {health_bonus} p i minskad hälsa."""
            y = ""
            z = self.get_stats()

            print_frame([w, x, y, z], self.color, 15)

    def get_stats(self):
        return f"{self.name} har {self.health} i hälsa och {self.attack} i attack."

    def update_health_by_city_mood(self, city, is_cpu, live):

        mood_score = calc_mood_score(self.mood, city, live=live)

        if mood_score is None:
            self.health += 20
            self.max_health += 20
        else:
            self.health += mood_score
            self.max_health += mood_score

        if is_cpu:
            w = f"{self.name} valde {city.capitalize()}. Tweet, tweet!"
        else:
            w = f"... Tweet, tweet! Beräknar humör för invånarna i {city.capitalize()} ..."

        x = f"{self.name} fick {mood_score} p i ökad hälsa! {self.catchword}"
        if mood_score is None:
            x = f"Något gick fel men {self.name} får 20 p i ökad hälsa! {self.catchword}"
        y = ""
        z = self.get_stats()
        print_frame([w, x, y, z], self.color, 15)

    def __repr__(self):
        return f'Poketer: {self.name} Mood: {self.mood}'


def choose_city():
    for idx, city in enumerate(geocodes):
        if city:
            print(idx + 1, city.capitalize())
    while True:
        try:
            city_choice = int(input(f"Vilken stad väljer du? (1-{len(geocodes) - 1}): "))
            if city_choice in range(1, len(geocodes)):
                break
        except ValueError:
            pass
        print(f"Ogiltligt val! Ange en siffra 1-{len(geocodes) - 1}.")

    # One of the elements in geocodes is an empty placeholder
    temp_city_list = list(geocodes)
    city_list = [x for x in temp_city_list if x != '']
    city = city_list[city_choice - 1]
    return city, city_list


def choose_emotion(city):
    for idx, emotion in enumerate(text_emotions):
        print(idx + 1, emotion.capitalize())
    while True:
        try:
            emotion_choice = int(
                input(f"Vilken känsla är mest förekommande i {city.capitalize()}? (1-{len(text_emotions)}): "))
            if emotion_choice in range(1, len(text_emotions) + 1):
                break
        except ValueError:
            pass
        print(f"Ogiltligt val! Ange en siffra 1-{len(text_emotions)}.")

    emotion_list = list(text_emotions)
    emotion = emotion_list[emotion_choice - 1]

    return emotion, emotion_list


def input_to_sentiment_analysis():
    while True:
        print(
            "Skriv in ett nyckelord att söka efter på Twitter. Endast bokstäver accepteras. Exempel: Donald Trump, Estonia.")
        keyword_choice = input(">> ")
        is_alphanumeric_or_space = (len([char for char in keyword_choice if not (char.isalpha() or char == " ")]) == 0)
        is_only_spaces = (len([char for char in keyword_choice if not char == " "]) == 0)
        if not is_alphanumeric_or_space or is_only_spaces or len(keyword_choice) < 1:
            continue

        while True:
            language_choice = input("Vilket språk vill du söka efter? [S]venska eller [E]ngelska? ")
            if language_choice.lower() == "s":
                language_choice = "swedish"
                break
            elif language_choice.lower() == "e":
                language_choice = "english"
                break

        while True:
            print(
                f"Tror du folket på Twitter är mest positivt, mest negativt eller neutralt inställda till {keyword_choice}?")
            attitude_choice = input("[P]ostiva - [N]egativa - ne[U]trala? ")
            if attitude_choice.lower() == "p":
                attitude_choice = "positivt"
                break
            elif attitude_choice.lower() == "n":
                attitude_choice = "negativt"
                break
            elif attitude_choice.lower() == "u":
                attitude_choice = "neutralt"
                break
        return keyword_choice, language_choice, attitude_choice


def chance_card_attack(user_pokemon, cpu, cpu_pokemon, live):
    attack_bonus = 20
    x = f"""
    Chanskort - attack! Välj en stad och gissa vilket humör som är mest förekommande bland invånarna.
    Gissar du rätt belönas din Poketer med {attack_bonus} p i ökad attack-styrka. Gissar du fel bestraffas din Poketer
    och förlorar {attack_bonus} p i attack-styrka. Lycka till!"""
    print_frame([x], 'white', 15)

    user_city, city_list = choose_city()
    user_emotion, emotion_list = choose_emotion(user_city)

    print("Det här kan ta en liten stund. Häng kvar! :)")
    most_frequent_emotions = mood_analysis(city=user_city, live=live)
    user_pokemon.attack_bonus(city=user_city, emotion=user_emotion, emotions=most_frequent_emotions, attack_bonus=attack_bonus)

    cpu_city = random.choice(city_list)
    cpu_emotion = random.choice(emotion_list)

    x = f"""{cpu.name} valde {cpu_city.capitalize()} och gissade på {cpu_emotion}."""
    print_frame([x], cpu_pokemon.color, 15)

    most_frequent_emotions = mood_analysis(city=cpu_city, live=live)
    cpu_pokemon.attack_bonus(city=cpu_city, emotion=cpu_emotion, emotions=most_frequent_emotions, attack_bonus=attack_bonus)

    input("\nTryck enter för att fortsätta")


def chance_card_health(user_pokemon):
    x = """
    Twitter-vadslagning! Har du koll på vad som trendar på sociala medier?
    Skriv in ett ord och på vilket språk du vill använda i sökningen. Gissa om
    de senaste tweetsen som innehåller detta ord är mest positiva, mest negativa
    eller neutrala. Om du gissar rätt belönas du med 10 p i ökad hälsa.
    Om du gissar fel bestraffas du med 10 p minskad hälsa. Lycka till!"""
    print_frame([x], 'white', 15)

    keyword_choice, language_choice, attitude_choice = input_to_sentiment_analysis()
    print("Det här kan ta en liten stund. Häng kvar! :)")

    result = sentiment_analysis(keyword=keyword_choice, language=language_choice,
                                file_name='demo_tweets_english_covid.p', live=True)

    user_pokemon.health_bonus(result=result, keyword=keyword_choice, attitude=attitude_choice)

    input("\nTryck enter för att fortsätta")


def card_attack(user, user_pokemon, cpu, cpu_pokemon):

    while (user_pokemon.health >= 0) and (cpu_pokemon.health >= 0):
        if user_pokemon.health <= 0 or cpu_pokemon.health <= 0:
            if cpu_pokemon.health <= 0:
                break
            if user_pokemon.health <= 0:
                print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu.name} vann! ***')
                break

        else:
            user_pokemon.attack_fnc(cpu_pokemon, cpu)
            if user_pokemon.healthcheck(cpu_pokemon, cpu.name) is False:
                break

            cpu_extra_s = (colored("s", cpu_pokemon.color))
            if cpu_pokemon.health > 0:
                print(f'*** Det är {cpu.name}{cpu_extra_s} tur ***')
                cpu_pokemon.attack_fnc(user_pokemon, user)
                if user_pokemon.healthcheck(cpu_pokemon, cpu.name) is False:
                    break


def card_block(user, user_pokemon, cpu, cpu_pokemon):

    while (user_pokemon.health >= 0) and (cpu_pokemon.health >= 0):

        if user_pokemon.health <= 0 or cpu_pokemon.health <= 0:
            if cpu_pokemon.health <= 0:
                break
            if user_pokemon.health <= 0:
                print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu.name} vann! ***')
                is_winner = False
                return is_winner

        else:
            user_pokemon.block(cpu, cpu_pokemon)
            if user_pokemon.healthcheck(cpu_pokemon, cpu.name) is False:
                break

            cpu_extra_s = (colored("s", cpu_pokemon.color))
            if cpu_pokemon.health > 0:
                print(f'*** Det är {cpu.name}{cpu_extra_s} tur ***')
                cpu_pokemon.attack_fnc(user_pokemon, user)
                if user_pokemon.healthcheck(cpu_pokemon, cpu.name) is False:
                    break

def intro_card(user_pokemon, cpu_pokemon, live):
    x = """
    Din Poketer har ett visst humör. Du har nu möjligheten att öka din Poketers hälsa
    genom att söka efter en stad i Sverige där du tror att invånarna är på samma humör som din Poketer.
    Invånarnas humör baseras på vad de twittrar. Ju mer känslosamma de är desto mer ökar
    din Poketers hälsa. Lycka till!"""
    print_frame([x], 'white', 15)

    user_city, city_list = choose_city()

    print("Det här kan ta en liten stund. Häng kvar! :)")
    user_pokemon.update_health_by_city_mood(user_city, is_cpu=False, live=live)

    cpu_city = random.choice(city_list)
    cpu_pokemon.update_health_by_city_mood(cpu_city, is_cpu=True, live=live)

    input("\nTryck enter för att fortsätta")


def game_choices(user, user_pokemon, cpu, cpu_pokemon, live):
    while True:
        print("\nVad vill du göra?")
        choices = {1: "Attackera", 2: "Blockera", 3: "Chanskort - attack", 4: "Chanskort - hälsa", 5: "Visa status",
                   6: "Avsluta spelet"}
        for choice in choices:
            print(choice, choices[choice])

        while True:
            try:
                user_choice = int(input(">> "))
                if user_choice in range(1, len(choices) + 1):
                    break
            except ValueError:
                pass
            print(f"Ange en siffra 1-{len(choices)}.")

        if user_choice == 1:
            x = "Attack! Nu är det dags för battle!"
            print_frame([x], 'white', 15)
            card_attack(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon)
        elif user_choice == 2:
            x = "Block! Nu är det dags för battle!"
            print_frame([x], 'white', 15)
            card_block(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon)
        elif user_choice == 3:
            print("Chanskort - attack")
            chance_card_attack(user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, live=live)
        elif user_choice == 4:
            print("Chanskort - hälsa!")
            chance_card_health(user_pokemon)
        elif user_choice == 5:
            print("Visar status")
            print("Dina Poketerer:")
            print(" -", user_pokemon.get_stats())
            print("Motståndarens Poketerer:")
            print(" -", cpu_pokemon.get_stats())
            input("\nTryck enter för att fortsätta")
        elif user_choice == 6:
            print("Avslutar spelet..")
            sys.exit(0)


def gameloop(live):
    draw_welcome_screen()
    username = input("Vänligen ange ditt namn: ")
    poketer_mood_explanation_text(username)

    input("\nTryck enter för att fortsätta")

    user_pokemon = Poketer(colored("Glada Gunnar", 'yellow'), 'happy', 'yellow', 50, 50, 45, catchword="#YOLO")
    user = User(colored(username, user_pokemon.color))
    user.add_team(user_pokemon)

    cpu_pokemon = Poketer(colored("Aggressiva Ada", 'red'), 'angry', 'red', 50, 50, 45, catchword="#FTW")
    cpu = User(colored("Olof", cpu_pokemon.color))
    cpu.add_team(cpu_pokemon)

    x = f"\n{user.name}, din Poketer är {user_pokemon.name}."
    y = user_pokemon.get_stats()
    print_frame([x, y], user_pokemon.color, 15)

    x = f"Din motståndare är {cpu.name} och har valt poketer {cpu_pokemon.name}."
    y = cpu_pokemon.get_stats()
    print_frame([x, y], cpu_pokemon.color, 15)

    input("\nTryck enter för att fortsätta")

    intro_card(user_pokemon=user_pokemon, cpu_pokemon=cpu_pokemon, live=live)

    is_winner = game_choices(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, live=live)

    is_winner = False
    if is_winner:
        x = "Grattis! Du vann! Lejon jämför sig inte med människor - Ibrahimovic."
        draw_end_screen(x, user_pokemon.color, 15)
    else:
        x = "Du förlorade! Du kan inte vinna om du inte lär dig hur man förlorar - Abdul-Jabbar."
        draw_end_screen(x, user_pokemon.color, 15)


if __name__ == '__main__':
    gameloop(live=False)
