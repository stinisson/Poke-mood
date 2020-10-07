"Pokemon Battle GO!"

class Poketer():
    def __init__(self, name, mood, health, attack):
        self.name = name
        self.mood = mood
        self.health = health
        self.attack = attack

user_pokemon = Poketer("Happy Hasse", "happy", 100, 25)
cpu_pokemon = Poketer("Aggressive Ada", "angry", 100, 25)

class User():
    def __init__(self, name, team):
        self.name = name
        self.team = team
self.team = []