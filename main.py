"Pokemon Battle GO!"


class Poketer:
    def __init__(self, name, mood, health, attack):
        self.name = name
        self.mood = mood
        self.health = health
        self.attack = attack


class User:
    def __init__(self, name, team =""):
        self.name = name
        self.team = []

    def add_team(self, poketer):
        self.team.append(poketer)


def main():
    user_pokemon = Poketer("Happy Hasse", "happy", 100, 25)
    cpu_pokemon = Poketer("Aggressive Ada", "angry", 100, 25)
    print(f"Du valde {user_pokemon.name}")
    print(f"Din motståndare valde {cpu_pokemon.name}")

    user = User("Martin")
    user.add_team(user_pokemon)


if __name__ == '__main__':
    main()