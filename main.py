import pygame
import random

pygame.init()

# 화면 설정
screen_height = 600
screen_width = 1300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("몬스터 잡기")

# 이미지 로드
warrior_jump_image = pygame.image.load("assets/warrior/jump/jump.png")
warrior_attack_image = pygame.image.load("assets/warrior/attack/attack.png")
warrior_running_image = [
    pygame.image.load('assets/warrior/run/run1.png'),
    pygame.image.load('assets/warrior/run/run2.png'),
    pygame.image.load('assets/warrior/run/run3.png'),
    pygame.image.load('assets/warrior/run/run4.png'),
    pygame.image.load('assets/warrior/run/run5.png'),
    pygame.image.load('assets/warrior/run/run6.png'),
    pygame.image.load('assets/warrior/run/run7.png'),
    pygame.image.load('assets/warrior/run/run8.png')
]

assassin_jump_image = pygame.image.load("assets/assassin/jump/jump.png")
assassin_attack_image = pygame.image.load("assets/assassin/attack/attack.png")
assassin_running_image = [
    pygame.image.load('assets/assassin/run/run1.png'),
    pygame.image.load('assets/assassin/run/run2.png'),
    pygame.image.load('assets/assassin/run/run3.png'),
    pygame.image.load('assets/assassin/run/run4.png'),
    pygame.image.load('assets/assassin/run/run5.png'),
    pygame.image.load('assets/assassin/run/run6.png'),
    pygame.image.load('assets/assassin/run/run7.png'),
    pygame.image.load('assets/assassin/run/run8.png')
]

mage_jump_image = pygame.image.load("assets/mage/jump/jump.png")
mage_attack_image = pygame.image.load("assets/mage/attack/attack.png")
mage_running_image = [
    pygame.image.load('assets/mage/run/run1.png'),
    pygame.image.load('assets/mage/run/run2.png'),
    pygame.image.load('assets/mage/run/run3.png'),
    pygame.image.load('assets/mage/run/run4.png'),
    pygame.image.load('assets/mage/run/run5.png'),
    pygame.image.load('assets/mage/run/run6.png'),
    pygame.image.load('assets/mage/run/run7.png'),
    pygame.image.load('assets/mage/run/run8.png')
]

goblin_image = pygame.image.load("assets/goblin/goblin.png")
ogre_image = pygame.image.load("assets/ogre/ogre.png")
orc_image = pygame.image.load("assets/orc/orc.png")

goblin_image = pygame.transform.scale(goblin_image, (60, 80))
ogre_image = pygame.transform.scale(ogre_image, (60, 80))
orc_image = pygame.transform.scale(orc_image, (60, 80))

bg = pygame.image.load("assets/background/background.png")


# Template Method Pattern
class Character:
    x_pos = 80
    y_pos = 340
    JUMP_VEL = 8.5

    def __init__(self, character_run_img, character_jump_img, character_attack_img):
        self.character_run_img = character_run_img
        self.character_jump_img = character_jump_img
        self.character_attack_img = character_attack_img

        self.running = True
        self.jumping = False
        self.attacking = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.character_run_img[0]
        self.character_rect = self.image.get_rect() # 피격 범위 설정
        self.character_rect.x = self.x_pos
        self.character_rect.y = self.y_pos
    
    def update(self, userInput):
        if self.jumping:
            self.jump()
        elif self.running:
            self.run()
        if self.attacking and not self.jumping:
            self.attack()

        if self.step_index >= 8:
            self.step_index = 0

        # 특정 입력값에 따라 캐릭터의 동작 제어
        if userInput[pygame.K_LALT] and not self.jumping: # 점프
            self.jumping = True
            self.attacking = False
            self.running = False
        elif userInput[pygame.K_LCTRL]: # 공격
            self.attacking = True
            self.running = False
        elif not (self.jumping or userInput[pygame.K_LCTRL]): # 달리기
            self.jumping = False
            self.attacking = False
            self.running = True

    def attack(self): # template method pattern 적용 부분
        pass

    def run(self):
        self.image = self.character_run_img[self.step_index]
        self.character_rect = self.image.get_rect()
        self.character_rect.x = self.x_pos
        self.character_rect.y = self.y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.character_jump_img
        if self.jumping:
            self.character_rect.y -= self.jump_vel * 3
            self.jump_vel -= 0.5
        if self.jump_vel < - self.JUMP_VEL:
            self.jumping = False
            self.jump_vel = self.JUMP_VEL
        
    def draw(self, screen):
        screen.blit(self.image, (self.character_rect.x, self.character_rect.y))


class Warrior(Character):
    def __init__(self, character_run_img, character_jump_img, character_attack_img):
        super().__init__(character_run_img, character_jump_img, character_attack_img)
        self.last_attack_time = 0
        self.attack_duration = 800

    def attack(self):
        current_time = pygame.time.get_ticks()  # 현재 시간을 ms 단위로 가져옴
        if current_time - self.last_attack_time >= self.attack_duration: # 쿨타임 설정
            self.image = self.character_attack_img
            self.character_rect = self.image.get_rect()
            self.character_rect.x = self.x_pos
            self.character_rect.y = self.y_pos - 15
            self.last_attack_time = current_time  # 현재 시간을 마지막 공격 시간으로 업데이트
            
            # 몬스터와의 충돌 감지 및 제거
            for monster in monsters:
                if monster.rect.x <= 300:
                    monsters.remove(monster)


class Dagger():
    def __init__(self, x, y):
        self.width = 20
        self.height = 5
        self.color = (128, 128, 128)
        self.x = x
        self.y = y
        self.speed = 15
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Assassin(Character):
    def __init__(self, character_run_img, character_jump_img, character_attack_img):
        super().__init__(character_run_img, character_jump_img, character_attack_img)
        self.daggers = []
        self.last_attack_time = 0  # 마지막 공격 시간을 저장할 변수 추가

    def attack(self):
        current_time = pygame.time.get_ticks()  # 현재 시간을 ms 단위로 가져옴
        # 현재 시간과 마지막 공격 시간의 차이가 300ms 이상이면 공격을 실행함
        if current_time - self.last_attack_time >= 300:
            self.image = self.character_attack_img
            self.character_rect = self.image.get_rect()  # 피격범위 생성
            self.character_rect.x = self.x_pos
            self.character_rect.y = self.y_pos - 15
            self.daggers.append(Dagger(self.character_rect.right, self.character_rect.centery))
            self.last_attack_time = current_time  # 현재 시간을 마지막 공격 시간으로 업데이트

    def update(self, userInput):
        super().update(userInput)
        for dagger in self.daggers:
            dagger.update()
        self.daggers = [dagger for dagger in self.daggers if dagger.rect.x < screen_width]

    def draw(self, screen):
        super().draw(screen)
        for dagger in self.daggers:
            dagger.draw(screen)


class Fireball:
    def __init__(self, x, y):
        self.radius = 10
        self.color = (255, 0, 0)  # 빨간색
        self.x = x
        self.y = y
        self.speed = 20
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Mage(Character):
    def __init__(self, character_run_img, character_jump_img, character_attack_img):
        super().__init__(character_run_img, character_jump_img, character_attack_img)
        self.fireballs = []
        self.last_attack_time = 0  # 마지막 공격 시간을 저장할 변수 추가

    def attack(self):
        current_time = pygame.time.get_ticks()  # 현재 시간을 ms 단위로 가져옴
        # 현재 시간과 마지막 공격 시간의 차이가 500ms 이상이면 공격을 실행함
        if current_time - self.last_attack_time >= 500:
            self.image = self.character_attack_img
            self.character_rect = self.image.get_rect()  # 피격범위 생성
            self.character_rect.x = self.x_pos
            self.character_rect.y = self.y_pos - 15
            self.fireballs.append(Fireball(self.character_rect.right, self.character_rect.centery))
            self.last_attack_time = current_time  # 현재 시간을 마지막 공격 시간으로 업데이트

    def update(self, userInput):
        super().update(userInput)
        for fireball in self.fireballs:
            fireball.update()
        self.fireballs = [fireball for fireball in self.fireballs if fireball.rect.x < screen_width]

    def draw(self, screen):
        super().draw(screen)
        for fireball in self.fireballs:
            fireball.draw(screen)


#Factory Method Pattern
class Factory:
    def create_character(self):
        pass
        
class WarriorFactory(Factory):
    def create_character(self, character_run_img, character_jump_img, character_attack_img):
        return Warrior(character_run_img, character_jump_img, character_attack_img)

class AssassinFactory(Factory):
    def create_character(self, character_run_img, character_jump_img, character_attack_img):
        return Assassin(character_run_img, character_jump_img, character_attack_img)

class MageFactory(Factory):
    def create_character(self, character_run_img, character_jump_img, character_attack_img):
        return Mage(character_run_img, character_jump_img, character_attack_img)
    

# Strategy Pattern
class CharacterSelector:
    def __init__(self, warrior, assassin, mage):
        self.characters = {
            'warrior': warrior,
            'assassin': assassin,
            'mage': mage
        }
        self.current_character = warrior

    def set_character(self, character_type):
        self.current_character = self.characters[character_type]

    def update(self, userInput):
        if userInput[pygame.K_1]:
            self.set_character('warrior')
        elif userInput[pygame.K_2]:
            self.set_character('mage')
        elif userInput[pygame.K_3]:
            self.set_character('assassin')
        self.current_character.update(userInput)

    def draw(self, screen):
        self.current_character.draw(screen)


class Monster():
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.hitpoints = 3
    
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            monsters.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Goblin(Monster):
    def __init__ (self, image):
        super().__init__(image)
        self.hitpoints = 1
        self.rect.y = 325
        
class Ogre(Monster):
    def __init__ (self, image):
        super().__init__(image)
        self.hitpoints = 3
        self.rect.y = 325

class Orc(Monster):
    def __init__ (self, image):
        super().__init__(image)
        self.hitpoints = 5
        self.rect.y = 325


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, monsters
    run = True
    clock = pygame.time.Clock()

    warriorFactory = WarriorFactory()
    assassinFactory = AssassinFactory()
    mageFactory = MageFactory()

    warrior = warriorFactory.create_character(warrior_running_image, warrior_jump_image, warrior_attack_image)
    assassin = assassinFactory.create_character(assassin_running_image, assassin_jump_image, assassin_attack_image)
    mage = mageFactory.create_character(mage_running_image, mage_jump_image, mage_attack_image)

    character_selector = CharacterSelector(warrior, assassin, mage)

    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.SysFont('malgungothic', 20)
    monsters = []

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("score: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = bg.get_width()
        screen.blit(bg, (x_pos_bg, y_pos_bg))
        screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        character_selector.draw(screen)
        character_selector.update(userInput)
        current_character = character_selector.current_character

        if len(monsters) == 0:
            monster_type = random.randint(0, 2)
            if monster_type == 0:
                monsters.append(Goblin(goblin_image))
            elif monster_type == 1:
                monsters.append(Ogre(ogre_image))
            else:
                monsters.append(Orc(orc_image))

        #몬스터 생성 & 충돌 감지
        for monster in monsters:
            monster.draw(screen)
            monster.update()
            if current_character.character_rect.colliderect(monster.rect):
                displaypoint()
                pygame.time.delay(2000)
                run = False
            elif isinstance(current_character, Mage):
                for fireball in current_character.fireballs:
                    if fireball.rect.colliderect(monster.rect):
                        monster.hitpoints -= 2
                        if monster.hitpoints <= 0:
                            monsters.remove(monster)
                        current_character.fireballs.remove(fireball)
            elif isinstance(current_character, Assassin):
                for dagger in current_character.daggers:
                    if dagger.rect.colliderect(monster.rect):
                        monster.hitpoints -= 1
                        if monster.hitpoints <= 0:
                            monsters.remove(monster)
                        current_character.daggers.remove(dagger)

        background()
        score()

        clock.tick(60)
        pygame.display.update()

def displaypoint():
    global points
    font = pygame.font.SysFont('malgungothic', 30)
    text = font.render('GAME OVER', True, (0,0,0))
    score = font.render("당신의 점수: " + str(points), True, (0,0,0))
    scoreRect = score.get_rect()
    scoreRect.center = (screen_width // 2, screen_height // 2 + 50)
    textRect = text.get_rect()
    textRect.center = (screen_width // 2, screen_height // 2)
    screen.blit(text, textRect)
    screen.blit(score, scoreRect)
    pygame.display.update()


def menu():
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont('malgungothic', 30)
        text = font.render('아무 키를 누르고 게임을 시작하세요.', True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, textRect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                main()
        
menu()

pygame.quit()
