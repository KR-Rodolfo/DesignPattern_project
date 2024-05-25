from dessign_pattern import Character, Warrior, Mage, Assassin

# Decorator 클래스
class CharacterDecorator(Character):
    def __init__(self, decorated_character: Character):
        super().__init__(
            hp=decorated_character.hp, 
            mp=decorated_character.mp, 
            attack=decorated_character.attack, 
            magic=decorated_character.magic
        )
        self.decorated_character = decorated_character

    def special_skill(self) -> str:
        return self.decorated_character.special_skill()

    def secondary_skill(self) -> str:
        return self.decorated_character.secondary_skill()

# 2차 전직
class SecondJobDecorator(CharacterDecorator):
    def __init__(self, decorated_character: Character):
        super().__init__(decorated_character)
        if isinstance(decorated_character, Warrior):
            self.hp += 150
            self.mp += 25
            self.attack += 100
            self.magic += 25
        elif isinstance(decorated_character, Mage):
            self.hp += 50
            self.mp += 100
            self.attack += 50
            self.magic += 100
        elif isinstance(decorated_character, Assassin):
            self.hp += 50
            self.mp += 50
            self.attack += 150
            self.magic += 50

    def special_skill(self) -> str:
        return "Upgraded " + self.decorated_character.special_skill()

# 3차 전직
class ThirdJobDecorator(CharacterDecorator):
    def __init__(self, decorated_character: Character):
        super().__init__(decorated_character)
        if isinstance(decorated_character, Warrior):
            self.hp += 200
            self.attack += 150
        elif isinstance(decorated_character, Mage):
            self.hp += 50
            self.mp += 150
            self.magic += 150
        elif isinstance(decorated_character, Assassin):
            self.hp += 50
            self.attack += 200
            self.mp += 100
            self.magic += 50

    def secondary_skill(self) -> str:
        return "Advanced " + self.decorated_character.secondary_skill()

