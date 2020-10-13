"""Pokemon Battle GO!"""
from mood_score import calc_mood_score
import sys
from random import randint
import time
from termcolor import colored, cprint
import colorama
colorama.init()


class Poketer:
    def __init__(self, name, mood, health, max_health, attack):
        self.name = name
        self.mood = mood
        self.health = health
        self.max_health = max_health
        self.attack = attack

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
            print(f"Hälsan för {self.name} ökade med {health_score}. Total hälsa: {self.max_health}\n")

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


def block():
    block_chance = randint(1, 11)
    if block_chance <= 7:
        time.sleep(1)
        print("Lyckad Block")
        block_sucess = True
    elif block_chance >= 8:
        time.sleep(1)
        print("Misslyckad Block")
        block_sucess = False
    return block_sucess


def delay_print(intro_text, s, a):
    print(intro_text)
    for i in s:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.4)
    print(a)
    time.sleep(0.5)


def main():
    user_pokemon = Poketer(colored("Happy Hasse", 'blue'), "happy", 100, 100, 25)
    cpu_pokemon = Poketer(colored("Aggressive Ada", 'red'), "angry", 100, 100, 25)

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
    print(f"Din motståndares poketer är {cpu_pokemon.name}.\n")
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

    print("*** Dags för battle! ***")

    while (user_pokemon.health >= 0) and (cpu_pokemon.health >= 0):
        if user_pokemon.health <= 0 or cpu_pokemon.health <= 0:
            if cpu_pokemon.health <= 0:
                print(f'*** Din motståndare svimmade. Du vann! ***')
                break
            if user_pokemon.health <= 0:
                print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu.name} vann! ***')
                break

        else:
            user_choose = int(input("Vill du [1] attackera eller [2] blockera? "))
            if user_choose == 1:
                cpu_pokemon.health -= user_pokemon.attack
                print(f"{user_pokemon.name} ==> Attackerade ==> {cpu_pokemon.name} ")
                print(f"{cpu_pokemon.name} hälsa: {cpu_pokemon.health}\n")
                user_pokemon.health -= cpu_pokemon.attack
                time.sleep(1)
                if user_pokemon.health <= 0 or cpu_pokemon.health <= 0:
                    if cpu_pokemon.health <= 0:
                        print(f'*** Din motståndare svimmade. Du vann! ***')
                        break
                    elif user_pokemon.health <= 0:
                        print(f'*** Din poketer {user_pokemon.name} svimmade. {cpu.name} vann! ***')
                        break
                else:
                    delay_print(f"{cpu.name} attackerade med {cpu_pokemon.name}", "3 2 1...", "Boom!")

                    print(f"{cpu_pokemon.name} ==> Attackerade ==> {user_pokemon.name} ")
            elif user_choose == 2:
                print(f"Du =/= Blockerar =/= ")
                x = block()
                if not x:
                    user_pokemon.health -= cpu_pokemon.attack
                    delay_print(f"{cpu.name} attackerade med {cpu_pokemon.name}", "3 2 1...", "Boom!")
                    print(f"{cpu_pokemon.name} ==> Attackerade ==> {user_pokemon.name} ")
                    print(f"{user_pokemon.name} tog {cpu_pokemon.attack} skada!")
                elif x:
                    user_pokemon.health -= cpu_pokemon.attack // 2
                    delay_print(f"{cpu.name} attackerade med {cpu_pokemon.name}", "3 2 1...", "Boom!")
                    print(f"{cpu_pokemon.name} ==> Attackerade ==> {user_pokemon.name} ")
                    print(f"{user_pokemon.name} tog {cpu_pokemon.attack // 2} skada!")

            if user_pokemon.health >= user_pokemon.max_health / 2:
                print(f"{user_pokemon.name} hälsa: {colored(user_pokemon.health, 'green')}\n")
            elif user_pokemon.max_health / 4 <= user_pokemon.health <= user_pokemon.max_health / 2:
                print(f"{user_pokemon.name} hälsa: {colored(user_pokemon.health, 'yellow')}\n")
            elif user_pokemon.health <= user_pokemon.max_health / 4:
                print(f"{user_pokemon.name} hälsa: {colored(user_pokemon.health, 'red')}\n")


if __name__ == '__main__':
    main()
