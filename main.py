"Pokemon Battle GO!"
from random import randint
import time
from termcolor import colored, cprint
import colorama
colorama.init()

class Poketer:
    def __init__(self, name, mood, health, attack):
        self.name = name
        self.mood = mood
        self.health = health
        self.attack = attack

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
        time.sleep(2)
        print("Lyckad Block")
        block_sucess = True
    elif block_chance >= 8:
        time.sleep(2)
        print("Misslyckad Block")
        block_sucess = False
    return block_sucess


def main():
    user_pokemon = Poketer(colored("Happy Hasse", 'blue'), "happy", 100, 25)
    cpu_pokemon = Poketer(colored("Aggressive Ada", 'red'), "angry", 100, 25)

    username = input("Vad heter du? ")
    user = User(colored(username, 'blue'))
    rival = input("Vad heter din motståndare? ")
    cpu = User(colored(rival, 'red'))
    user.add_team(user_pokemon)
    cpu.add_team(cpu_pokemon)
    print(f"Hej {user.name}. Din poketer är {user_pokemon.name}")
    print(f"Din motståndares poketer är {cpu_pokemon.name}\n")
    print(f"{user.name}, det är din tur! ")
    print(f"Välj en stad du tror att det är mycket {user_pokemon.mood} content i.")

    happy_city_dic = {"Göteborg": 25, "Stockholm": 5}  # Namn+gläjde
    angry_city_dic = {"Göteborg": 5, "Stockholm": 25}

    city = input("Välj mellan Göteborg eller Stockholm: ")
    print("\nBeräknar mood'content...")

    if city == "Göteborg":
        user_pokemon.health += happy_city_dic["Göteborg"]
        cpu_pokemon.health += angry_city_dic['Stockholm']
        print(f"{user.name} valde {city} med mycket happy-content!")
        print(f"Happy Hasse hälsa ökade med {happy_city_dic['Göteborg']}. Total hälsa: {user_pokemon.health}\n")

        print(f"{cpu.name} valde Stockholm med mycket angry-content!")
        print(f"Aggressive Ada hälsa ökade med {angry_city_dic['Stockholm']}. Total hälsa: {cpu_pokemon.health}\n")

    elif city == "Stockholm":
        user_pokemon.health += happy_city_dic["Stockholm"]
        cpu_pokemon.health += angry_city_dic['Göteborg']
        print(f"{user.name} valde {city} med inte så mycket happy-content.")
        print(f"Happy Hasse hälsa ökade med {happy_city_dic['Stockholm']}. Total hälsa: {user_pokemon.health}\n")

        print(f"{cpu.name} valde Göteborg med inte så mycket angry-content.")
        print(f"Aggressive Ada hälsa ökade med {angry_city_dic['Göteborg']}. Total hälsa: {cpu_pokemon.health}\n")

    print("*** Dags för battle! ***")
    while True:
        user_choose = int(input("Vill du [1] attackera eller [2] blockera? "))
        if user_choose == 1:
            cpu_pokemon.health -= user_pokemon.attack
            print(f"Du ==> Attackerade ==> {cpu_pokemon.name} ")
            print(f"Aggressive Ada hälsa: {cpu_pokemon.health}\n")
            user_pokemon.health -= cpu_pokemon.attack
            time.sleep(2)
            print(f"{cpu_pokemon.name} ==> Attackerade ==> {user_pokemon.name} ")
        elif user_choose == 2:
            print(f"Du =/= Blockerar =/= ")
            x = block()
            if x == False:
                user_pokemon.health -= cpu_pokemon.attack
                print(f"{cpu_pokemon.name} ==> Attackerade ==> {user_pokemon.name} ")
                print(f"Du tog {cpu_pokemon.attack} skada!")
            elif x == True:
                user_pokemon.health -= cpu_pokemon.attack // 2
                print(f"{cpu_pokemon.name} ==> Attackerade ==> {user_pokemon.name} ")
                print(f"Du tog {cpu_pokemon.attack // 2} skada!")

        if cpu_pokemon.health <= 0:
            print(f'*** Din motståndare svimmade. Du vann! ***')
            break

        current_hp = 125

        if user_pokemon.health >= current_hp / 2:
            print(f"Din hälsa: {colored(user_pokemon.health, 'green')}\n")
        elif current_hp / 4 <= user_pokemon.health <= current_hp / 2:
            print(f"Din hälsa: {colored(user_pokemon.health, 'yellow')}\n")
        elif user_pokemon.health <= current_hp / 4:
            print(f"Din hälsa: {colored(user_pokemon.health, 'red')}\n")

        if user_pokemon.health <= 0:
            print(f'*** Din poketer svimmade. {cpu.name} vann! ***')
            break


if __name__ == '__main__':
    main()
