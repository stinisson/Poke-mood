"""Pokemon Battle GO!"""
from mood_score import calc_mood_score
import sys
from random import randint
import time
from termcolor import colored, cprint
import colorama
colorama.init()
from prints_module import delay_print, atk_txt
#TODO:
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
        if self.health >= self.max_health / 2:
                print(f"{self.name} hälsa: {colored(self.health, 'green')}\n")
        elif self.max_health / 4 <= self.health <= self.max_health / 2:
                print(f"{self.name} hälsa: {colored(self.health, 'yellow')}\n")
        elif self.health <= self.max_health / 4:
                print(f"{self.name} hälsa: {colored(self.health, 'red')}\n")


    def block(self, opponent, opponent_pokemon):
        block_chance = randint(1, 11)
        if block_chance <= 7:
            time.sleep(1)
            print(f"{self.name} =|= Blockerar =|= {(colored('Lyckad Block', 'green'))}\n")
            self.health -= opponent_pokemon.attack // 2
            delay_print(f"{opponent.name} attackerade med {opponent_pokemon.name}", "3 2 1...", "Boom!")
            print(f"{opponent_pokemon.name} ==> Attackerade ==> {self.name}\n")
            print(f"{self.name} tog {opponent_pokemon.attack // 2} i skada!")
        elif block_chance >= 8:
            time.sleep(1)
            print(f"{self.name} =|= Blockerar =|= {(colored('Misslyckad Block', 'red'))}\n")
            self.health -= opponent_pokemon.attack
            delay_print(f"{opponent.name} attackerade med {opponent_pokemon.name}", "3 2 1...", "Boom!")
            print(f"{opponent_pokemon.name} ==> Attackerade ==> {self.name}\n")
            print(f"{self.name} tog {opponent_pokemon.attack} i skada!")


    def update_max_health_by_city_mood(self, city, user_name):
        mood_score = calc_mood_score(self.mood, city)
        if mood_score == -1:
            print("Tyvärr denna staden är ej tillgänglig, men du får 20 extra i hälsa. ")
            self.max_health += 20
            self.health += 20
        else:
            health_score = round(mood_score * self.health)
            self.health += health_score
            self.max_health += health_score
            print(f"{user_name} valde {city} med mycket {self.mood}-content!")
            print(f"Hälsan för {self.name} ökade med {health_score}. Total hälsa: {colored(self.max_health, 'green')}\n")

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

    print(f"Välj en stad du tror att det är mycket {user_pokemon.mood} content i.")
    city = input("Välj mellan Göteborg eller Stockholm: ")
    delay_print("Beräknar mood'content", ".....", "")

    if city == "Göteborg":
        user_pokemon.update_max_health_by_city_mood("Göteborg", user.name)
        cpu_pokemon.update_max_health_by_city_mood("Stockholm", cpu.name)

    elif city == "Stockholm":
        user_pokemon.update_max_health_by_city_mood("Stockholm", user.name)
        cpu_pokemon.update_max_health_by_city_mood("Göteborg", cpu.name)

    else:
        print("Tyvärr denna staden är ej tillgänglig, men du får 20 extra i hälsa. ")
        user_pokemon.max_health += 20
        user_pokemon.health += 20
        print(f"Hälsan för {user_pokemon.name} ökade med 20. Total hälsa: {colored(user_pokemon.max_health, 'green')}\n")
        cpu_pokemon.update_max_health_by_city_mood("Stockholm", cpu.name)

    print("*** Dags för battle! ***")

    while (user_pokemon.health >= 0) and (cpu_pokemon.health >= 0):
        if user_pokemon.health <= 0 or cpu_pokemon.health <= 0:
            if cpu_pokemon.health <= 0:

                break
            if user_pokemon.health <= 0:
                print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu.name} vann! ***')
                break

        else:
            print(f"{user.name}, det är din tur ! ")
            user_choose = int(input("Vill du [1] attackera eller [2] blockera? "))
            if user_choose == 1:
                user_pokemon.attack_fnc(cpu_pokemon)


                time.sleep(1)
                if user_pokemon.health <= 0 or cpu_pokemon.health <= 0:
                    if cpu_pokemon.health > 0:
                        print(f'*** Det är {cpu.name} tur.. ***')
                        cpu_pokemon.attack_fnc(user_pokemon)
                    elif user_pokemon.health <= 0:
                        print(f'*** {cpu.name} poketer {cpu_pokemon.name} svimmade. Du vann!! ***')
                        break

            elif user_choose == 2:
                user_pokemon.block(cpu, cpu_pokemon)


if __name__ == '__main__':
    main()
