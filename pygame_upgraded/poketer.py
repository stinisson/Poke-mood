import time
from random import randint
from termcolor import colored
#from prints_module import atk_txt, delay_print, successful_block, unsuccessful_block


class Poketer:
    def __init__(self, name, mood, color, health, max_health, attack, catchword):
        self.name = name
        self.mood = mood
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.color = color
        self.catchword = catchword

    def attack_fnc(self, opponent_pokemon):
        miss_chance = randint(1, 6)
        if miss_chance <= 5:
            opponent_pokemon.health -= self.attack
            atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
            self.healtcheck_color(opponent_pokemon)
            # self.healthcheck(opponent_pokemon, opponent.name)
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

    def block(self, opponent_pokemon):
        misschans = randint(1, 6)
        critchance = randint(1, 6)
        dmg_modifier = randint(-3, 3)
        if misschans <= 5:
            if critchance >= 4:
                opponent_pokemon.health -= (self.attack + dmg_modifier) * 2
                atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
                self.healtcheck(opponent_pokemon)
            elif critchance < 4:
                opponent_pokemon.health -= (self.attack + dmg_modifier)
                atk_txt(self.name, opponent_pokemon.name, "3 2 1...")
                self.healtcheck(opponent_pokemon)
        else:
            print(f"{opponent_pokemon.name} missade sin attack...")

    def add_attack(self, attack_score):
        self.attack += attack_score

    def add_health(self, health_score):
        self.health += health_score

    def add_max_health(self, max_health_score):
        self.max_health += max_health_score

    def get_attack(self):
        return self.attack

    def get_health(self):
        return self.health

    def get_stats(self):
        return f"{self.name} har {self.health} i hälsa och {self.attack} i attack."

    def set_attack(self, attack_score):
        self.attack = attack_score

    def __repr__(self):
        return f'Poketer: {self.name}. Mood: {self.mood}. Health: {self.health}. Max health: {self.max_health}. Attack: {self.attack}.'
