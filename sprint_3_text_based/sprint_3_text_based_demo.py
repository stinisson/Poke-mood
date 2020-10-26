"""Pokemon Battle GO!"""
from twitter_search import geocodes
from mood_score import calc_mood_score
from mood_analysis import mood_analysis, text_emotions
from sentiment_analysis import sentiment_analysis
from quiz import quiz
from user import User
from poketer import Poketer
import random
from termcolor import colored
import colorama
import sys
import warnings


colorama.init()
from print_module import delay_print, atk_txt, successful_block, unsuccessful_block, print_frame, draw_welcome_screen, \
    print_frame_with_newline, poketer_mood_explanation_text, draw_end_screen


def take_integer_input(input_text, end_range, error_text):
    while True:
        try:
            user_choice = int(input(input_text))
            if user_choice in range(1, end_range):
                break
        except ValueError:
            pass
        print(error_text)
    return user_choice


def choose_city():
    for idx, city in enumerate(geocodes):
        if city:
            print(idx + 1, city.capitalize())

    city_choice = take_integer_input(f"Vilken stad väljer du? (1-{len(geocodes) - 1}): ",
                                     len(geocodes), f"Ogiltligt val! Ange en siffra 1-{len(geocodes) - 1}.")

    # One of the elements in geocodes is an empty placeholder
    temp_city_list = list(geocodes)
    city_list = [x for x in temp_city_list if x != '']
    city = city_list[city_choice - 1]
    return city


def get_cities():
    temp_city_list = list(geocodes)
    cities = [x for x in temp_city_list if x != '']
    return cities


def choose_emotion(city):
    for idx, emotion in enumerate(text_emotions):
        print(idx + 1, emotion.capitalize())

    emotion_choice = take_integer_input(
        f"Vilken känsla är mest förekommande i {city.capitalize()}? (1-{len(text_emotions)}): ",
        len(text_emotions) + 1,
        f"Ogiltligt val! Ange en siffra 1-{len(text_emotions)}.")

    emotion_list = list(text_emotions)
    emotion = emotion_list[emotion_choice - 1]
    return emotion


def get_emotions():
    emotions = list(text_emotions)
    return emotions


def intro_card(poketer, is_cpu, live):
    if is_cpu:
        cities = get_cities()
        city = random.choice(cities)
    else:
        x = """
        Din Poketer har ett visst humör. Du har nu möjligheten att öka din Poketers hälsa
        genom att söka efter en stad i Sverige där du tror att invånarna är på samma humör som din Poketer.
        Invånarnas humör baseras på vad de twittrar. Ju mer känslosamma de är desto mer ökar
        din Poketers hälsa. Lycka till!"""
        print_frame([x], 'white', 15)
        city = choose_city()

    print("Det här kan ta en liten stund. Häng kvar! :)")

    mood_score = calc_mood_score(poketer.mood, city, live=live)

    if mood_score is None:
        poketer.add_health(20)
        poketer.add_max_health(20)
    else:
        poketer.add_health(mood_score)
        poketer.add_max_health(mood_score)

    if is_cpu:
        w = f"{poketer.name} valde {city.capitalize()}. Tweet, tweet!"
    else:
        w = f"... Tweet, tweet! Beräknar humör för invånarna i {city.capitalize()} ..."

    x = f"{poketer.name} fick {mood_score} p i ökad hälsa! {poketer.catchword}"
    if mood_score is None:
        x = f"Något gick fel men {poketer.name} får 20 p i ökad hälsa! {poketer.catchword}"
    y = ""
    z = poketer.get_stats()
    print_frame([w, x, y, z], poketer.color, 15)

    input("\nTryck enter för att fortsätta")


def card_attack(user_pokemon, cpu, cpu_pokemon, is_cpu):
    if is_cpu:
        x = f"{cpu.name} valde att attackera!"
        print_frame([x], cpu_pokemon.color, 15)
    else:
        x = "Du valde att attackera! Nu är det dags för battle!"
        print_frame([x], user_pokemon.color, 15)

    input("\nTryck enter för att fortsätta\n")

    if is_cpu:
        cpu_pokemon.attack_fnc(user_pokemon)
        if user_pokemon.get_health() <= 0:
            print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu_pokemon.name} vann! ***')
    else:
        user_pokemon.attack_fnc(cpu_pokemon)
        if cpu_pokemon.get_health() <= 0:
            print(f'*** Din motståndares Poketer {cpu_pokemon.name} svimmade. {user_pokemon.name} vann! ***')

    input("\nTryck enter för att fortsätta\n")


def card_block(user, user_pokemon, cpu, cpu_pokemon, is_cpu):
    if is_cpu:
        x = f"{cpu.name} valde att blocka!"
        print_frame([x], cpu_pokemon.color, 15)
    else:
        x = "Du valde block! Nu är det dags för battle!"
        print_frame([x], user_pokemon.color, 15)

    input("\nTryck enter för att fortsätta\n")

    if is_cpu:
        cpu_pokemon.block(user, user_pokemon)
        if cpu_pokemon.get_health() <= 0:
            print(f'*** Din motståndares Poketer {cpu_pokemon.name} svimmade. {user_pokemon.name} vann! ***')
    else:
        user_pokemon.block(cpu, cpu_pokemon)
        if user_pokemon.get_health() <= 0:
            print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu_pokemon.name} vann!')

    input("\nTryck enter för att fortsätta\n")


def chance_card_attack(player, poketer, is_cpu, live):
    attack_bonus = 20
    if is_cpu:
        cities = get_cities()
        city = random.choice(cities)
        emotions = get_emotions()
        emotion = random.choice(emotions)
        x = f"{player.name} valde chanskort - attack!"
        if emotion == 'ledsen':
            y = f"""{player.name} gissar att invånarna i {city.capitalize()} är ledsna."""
        else:
            y = f"""{player.name} gissar att invånarna i {city.capitalize()} är {emotion}a."""
        print_frame([x, y], poketer.color, 15)
    else:
        x = f"""
        Chanskort - attack! Välj en stad och gissa vilket humör som är mest förekommande bland invånarna.
        Gissar du rätt belönas din Poketer med {attack_bonus} p i ökad attack-styrka. Gissar du fel bestraffas din Poketer
        och förlorar {attack_bonus} p i attack-styrka. Lycka till!"""
        print_frame([x], 'white', 15)
        city = choose_city()
        emotion = choose_emotion(city)

    print("\nDet här kan ta en liten stund. Häng kvar! :)")
    most_frequent_emotions = mood_analysis(city=city, live=live)

    if emotion in most_frequent_emotions:
        poketer.add_attack(attack_bonus)
        w = f"""Det var rätt! I {city.capitalize()} är man {emotion}."""
        x = f"""{poketer.name} får {attack_bonus} p i ökad attack-styrka!"""
    else:
        poketer.add_attack(-attack_bonus)
        if poketer.get_attack() < 0:
            poketer.set_attack(0)
        w = f"Det var fel! I {city.capitalize()} är man {most_frequent_emotions[0]}, inte {emotion}!"
        x = f"{poketer.name} bestraffas med {attack_bonus} p i minskad attack-styrka."
    y = ""
    z = poketer.get_stats()

    print_frame([w, x, y, z], poketer.color, 15)
    input("\nTryck enter för att fortsätta")


def input_to_chance_card_health(is_cpu, user_select_from_fallback):
    keywords = {"Belarus": "tweets_belarus.p",
                "Biden": "tweets_biden.p",
                "COVID": "tweets_covid.p",
                "Donald Trump": "tweets_donald_trump.p",
                "Erdos number": "tweets_erdos_number.p",
                "Nobel Prize": "tweets_nobel_prize.p",
                "Poland": "tweets_poland.p",
                "Puppies": "tweets_puppies.p"}
    attitudes = ["positivt", "negativt", "neutralt"]
    file_name = ""

    if is_cpu:
        keyword_choice, file_name = random.choice(list(keywords.items()))
        attitude_choice = random.choice(attitudes)
        language_choice = "english"
        warnings.filterwarnings("ignore")
        return keyword_choice, language_choice, attitude_choice, file_name

    # If not possible to get tweets live, let user select from list with saved keyword files
    elif user_select_from_fallback:
        for idx, keyword in enumerate(keywords):
            print(idx + 1, keyword)

        keyword_choice = take_integer_input(f"Vilket sökord väljer du? (1-{len(keywords)}): ",
                                            len(keywords) + 1, f"Ogiltligt val! Ange en siffra 1-{len(keywords)}.")
        keyword_list = list(keywords)
        keyword_choice = keyword_list[keyword_choice - 1]

        language_choice = "english"
        while True:
            print(
                f"Tror du folket på engelskspråkiga Twitter är mest positivt, mest negativt eller neutralt inställda till {keyword_choice}?")
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
        return keyword_choice, language_choice, attitude_choice, file_name

    else:
        while True:
            print(
                "Skriv in ett nyckelord att söka efter på Twitter. Endast bokstäver accepteras. Exempel: Donald Trump, Estonia.")
            keyword_choice = input(">> ")
            is_alphanumeric_or_space = (
                    len([char for char in keyword_choice if not (char.isalpha() or char == " ")]) == 0)
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
            return keyword_choice, language_choice, attitude_choice, file_name


def chance_card_health(player, poketer, is_cpu):
    health_bonus = 10
    if is_cpu:
        x = f"{player.name} valde chanskort - hälsa!"
        print_frame([x], poketer.color, 15)
    else:
        x = f"""
        Twitter-vadslagning! Har du koll på vad som trendar på sociala medier?
        Skriv in ett ord och vilket språk du vill använda i sökningen. Gissa om
        de senaste tweetsen som innehåller detta ord är mest positiva, mest negativa
        eller neutrala. Om du gissar rätt belönas du med {health_bonus} p i ökad hälsa.
        Om du gissar fel bestraffas du med {health_bonus} p minskad hälsa. Lycka till!"""
        print_frame([x], 'white', 15)

    user_select_from_fallback = False
    while True:
        keyword, language, attitude, file_name = input_to_chance_card_health(is_cpu, user_select_from_fallback)

        if is_cpu:
            x = f"""{player.name} gissar att {keyword} har mest {attitude} innehåll på engelskspråkiga Twitter."""
            print_frame([x], poketer.color, 15)
            print("Det här kan ta en liten stund. Häng kvar! :)")
            result = sentiment_analysis(keyword=keyword, language=language,
                                        file_name=file_name, live=False)
        else:
            print("Det här kan ta en liten stund. Häng kvar! :)")
            result = sentiment_analysis(keyword=keyword, language=language,
                                        file_name='demo_tweets_english_covid.p', live=True)

        if result == 'connection_error':
            x = """Det går tyvärr inte att söka på Twitter just nu. Du får istället testa dina kunskaper
             på ett förvalt sökord på engelskspråkiga Twitter."""
            print_frame([x], 'white', 15)
            user_select_from_fallback = True
            continue

        if result == 'too_few_results':
            if is_cpu:
                x = f"Tyvärr, hittade för få tweets innehållandes {keyword}."
                print_frame([x], 'white', 15)
                return
            else:
                x = f"""Hittade för få tweets innehållandes {keyword}. Ett tips är att söka efter något som är
    mer aktuellt i samhällsdebatten."""
                print_frame([x], 'white', 15)
        else:
            break

    if result != 'connection_error':
        if attitude == result:
            poketer.add_health(health_bonus)
            poketer.add_max_health(health_bonus)
            w = f"Rätt! {keyword} har mest {result} innehåll på Twitter."
            x = f"{poketer.name} belönas med {health_bonus} p i ökad hälsa!"
        else:
            poketer.add_health(-health_bonus)
            poketer.add_max_health(-health_bonus)
            w = f"""Det var fel, {keyword} har mest {result} innehåll på Twitter!"""
            x = f"""{poketer.name} bestraffas med {health_bonus} p i minskad hälsa."""
        y = ""
        z = poketer.get_stats()

        print_frame([w, x, y, z], poketer.color, 15)

    input("\nTryck enter för att fortsätta")


def show_stats_card(user, cpu):
    print("\nVisar status")

    print("Dina Poketerer:")
    for poketer in user.team:
        print(" -", poketer.get_stats())

    print("Motståndarens Poketerer:")
    for poketer in cpu.team:
        print(" -", poketer.get_stats())
    input("\nTryck enter för att fortsätta")


def cpu_make_move(user, user_pokemon, cpu, cpu_pokemon, live):
    cpu_extra_s = (colored("s", cpu_pokemon.color))
    print(f"\nNu är det {cpu.name}{cpu_extra_s} tur!")

    # TODO implement cpu make quiz move
    #moves = ["attack", "block", "chance_card_attack", "chance_card_health", 'quiz']
    moves = ["attack", "block", "chance_card_attack", "chance_card_health"]

    move = random.choice(moves)

    if move == "attack":
        card_attack(user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=True)

    elif move == "block":
        card_block(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=True)

    elif move == "chance_card_attack":
        chance_card_attack(player=cpu, poketer=cpu_pokemon, is_cpu=True, live=live)

    elif move == "chance_card_health":
        chance_card_health(player=cpu, poketer=cpu_pokemon, is_cpu=True)

    # elif move == "quiz":
    #     quiz_card(player=cpu, poketer=cpu_pokemon, is_cpu=True)


def check_is_winner(user, cpu):
    for poketer in user.team:
        if poketer.get_health() <= 0:
            user.team.remove(poketer)

    for poketer in cpu.team:
        if poketer.get_health() <= 0:
            cpu.team.remove(poketer)

    if len(user.team) == 0:
        return "cpu"
    elif len(cpu.team) == 0:
        return "user"
    else:
        return None


def quiz_card(player, poketer, is_cpu, available_poketers):

    if is_cpu:
        x = f"""{player.name} valde quiz och har nu chansen att vinna en till Poketer! """
        print_frame([x], poketer.color, 15)
    else:
        x = f"""
        Quiz-dags! Om du svarar rätt på alla quiz-frågor får du välja en till Poketer. Frågekategorierna som finns
är datorer, matematik och vetenskap/natur. Kategorierna väljs slumpmässigt. Lycka till!"""
        print_frame([x], 'white', 15)

    input("\nTryck enter för att fortsätta\n")

    won_a_poketer = quiz()

    input("\nTryck enter för att fortsätta\n")

    if won_a_poketer:
        x = f"""Bra jobbat! Du har vunnit en ny Poketer!"""
        print_frame([x], poketer.color, 15)
        quiz_poke = choose_poketer(available_poketers, is_cpu=False)
        if quiz_poke is not None:
            player.add_team(quiz_poke)
    else:
        x = f"""Tyvärr! Du hade inte alla rätt på quizet så du vann inte en till Poketer. Bättre lycka nästa gång!"""
        print_frame([x], poketer.color, 15)

    input("\nTryck enter för att fortsätta\n")


def game_loop(user, user_pokemon, cpu, cpu_pokemon, live, available_poketers):
    while True:
        print("\nVad vill du göra?")
        choices = {1: "Attackera", 2: "Blockera", 3: "Chanskort - attack", 4: "Chanskort - hälsa",
                   5: "Quiz - vinn en ny Poketer", 6: "Visa status", 7: "Avsluta spelet"}

        for choice in choices:
            print(choice, choices[choice])

        user_choice = take_integer_input(f">> ", len(choices) + 1, f"Ange en siffra 1-{len(choices)}.")

        if user_choice == 1:
            card_attack(user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=False)

        elif user_choice == 2:
            card_block(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, is_cpu=False)

        elif user_choice == 3:
            chance_card_attack(player=user, poketer=user_pokemon, is_cpu=False, live=live)

        elif user_choice == 4:
            chance_card_health(player=user, poketer=user_pokemon, is_cpu=False)

        elif user_choice == 5:
            quiz_card(player=user, poketer=user_pokemon, is_cpu=False, available_poketers=available_poketers)

        elif user_choice == 6:
            show_stats_card(user=user, cpu=cpu)
            continue

        elif user_choice == 7:
            print("Avslutar spelet..")
            sys.exit(0)

        is_winner = check_is_winner(user=user, cpu=cpu)
        if is_winner is None:
            pass
        else:
            return is_winner

        cpu_make_move(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, live=live)

        is_winner = check_is_winner(user=user, cpu=cpu)
        if is_winner is None:
            pass
        else:
            return is_winner


def choose_poketer(available_poketers, is_cpu):
    if is_cpu:
        cpu_pokemon = random.choice(available_poketers)
        available_poketers.remove(cpu_pokemon)
        return cpu_pokemon
    else:
        print("Du ska nu få välja en Poketer. Dessa Pokteter är tillgängliga:")
        if len(available_poketers) > 0:
            for idx, poketer in enumerate(available_poketers):
                print(idx + 1, poketer.name)

            poketer_choice = take_integer_input(f"Vilken Poketer väljer du? (1-{len(available_poketers)}): ",
                                                len(available_poketers) + 1,
                                                f"Ogiltligt val! Ange en siffra 1-{len(available_poketers)}.")

            user_pokemon = available_poketers[poketer_choice - 1]
            available_poketers.remove(user_pokemon)
            return user_pokemon
        else:
            print("Tyvärr, det finns inga Poketerer kvar att välja bland.")
            return None



def start_game(live):
    draw_welcome_screen()
    username = input("Vänligen ange ditt namn: ")
    poketer_mood_explanation_text(username)
    input("\nTryck enter för att fortsätta\n")

    gunnar = Poketer(colored("Glada Gunnar", 'yellow'), 'happy', 'yellow', 50, 50, 45, catchword="#YOLO")
    ada = Poketer(colored("Aggressiva Ada", 'red'), 'angry', 'red', 50, 50, 45, catchword="#FTW")
    louise = Poketer(colored("Ledsna Louise", 'blue'), 'sad', 'blue', 50, 50, 45, catchword="#TGIF")
    kalle = Poketer(colored("Kärleksfulla Kalle", 'magenta'), 'loving', 'magenta', 50, 50, 45, catchword="#XOXO")
    available_poketers = [gunnar, ada, louise, kalle]

    user_pokemon = choose_poketer(available_poketers, is_cpu=False)
    cpu_pokemon = choose_poketer(available_poketers, is_cpu=True)

    user = User(colored(username, user_pokemon.color))
    user.add_team(user_pokemon)

    cpu = User(colored("Olof", cpu_pokemon.color))
    cpu.add_team(cpu_pokemon)

    x = f"\n{user.name}, din Poketer är {user_pokemon.name}."
    y = user_pokemon.get_stats()
    print_frame([x, y], user_pokemon.color, 15)

    x = f"Din motståndare är {cpu.name}. {cpu.name} valde poketer {cpu_pokemon.name}. {cpu_pokemon.get_stats()}"
    print_frame([x], cpu_pokemon.color, 15)

    input("\nTryck enter för att fortsätta")

    intro_card(poketer=user_pokemon, is_cpu=False, live=live)
    intro_card(poketer=cpu_pokemon, is_cpu=True, live=live)

    is_winner = game_loop(user=user, user_pokemon=user_pokemon, cpu=cpu, cpu_pokemon=cpu_pokemon, live=live, available_poketers=available_poketers)

    if is_winner == "user":
        x = "Grattis! Du vann! Lejon jämför sig inte med människor - Ibrahimovic."
        draw_end_screen(x, user_pokemon.color, 15)
    else:
        x = "Du förlorade! Du kan inte vinna om du inte lär dig hur man förlorar - Abdul-Jabbar."
        draw_end_screen(x, user_pokemon.color, 15)


if __name__ == '__main__':
    start_game(live=False)
