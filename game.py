import parameters as p
from button import *
from enemy import *
from object import *
from effects import *
from images import *


class Game:
    def __init__(self):
        pygame.display.set_caption('Ny pogodi')
        pygame.display.set_icon(icon)

        pygame.mixer_music.load('music/muz.mp3')
        pygame.mixer_music.set_volume(0.2)

        self.block_options = [60, 430, 54, 400, 60, 421]
        self.img_counter = 0
        self.health = 2
        self.energy = 2
        self.jump_counter = 30
        self.scores = 0
        self.max_scores = 0
        self.max_above = 0
        self.cooldown = 0
        self.make_jump = False

    def show_menu(self):
        pygame.mixer_music.pause()
        pygame.mixer.Sound.play(menu_sound)
        pygame.mixer.Sound.play(menu_sound, -1)
        menu_sound.set_volume(0.2)

        start_btn = Button(200, 50)
        quit_btn = Button(120, 50)

        show = True

        while show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.blit(fon, (0, 0))
            display.blit(menu_bckgr, (0, 0))
            display.blit(ny, (195, 50))

            if self.img_counter == 36:
                self.img_counter = 0
            display.blit(volk_img[self.img_counter // 6], (280, 130))
            self.img_counter += 1
            start_btn.draw(300, 350, '   Start game', self.start_game)
            quit_btn.draw(340, 410, '   Quit', quit)
            pygame.display.update()
            clock.tick(60)

    def start_game(self):
        self.health = 2
        self.energy = 2

        while self.game_cycle():
            self.scores = 0
            self.health = 2
            self.make_jump = False
            self.jump_counter = 30
            p.usr_y = display_height - usr_height - 110
            self.cooldown = 0

    def game_cycle(self):

        pygame.mixer_music.play(-1)

        game = True
        block_arr = []
        self.create_block_arr(block_arr)

        heart = Object(display_width, 220, 30, health_img, 4)
        energ = Object(display_width, 220, 30, energy_img, 4)

        all_btn_bullets = []
        all_ms_bullets = []

        zaych1 = Enemies(-150)

        all_enemies = [zaych1]

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if keys[pygame.K_SPACE]:
                self.make_jump = True
            if keys[pygame.K_ESCAPE]:
                menu_sound.set_volume(0.2)
                self.pause()

            if self.make_jump:
                self.jump()

            self.count_scores(block_arr)

            display.blit(land, (0, 0))
            print_text1('Score: ' + str(self.scores), 15, 550)

            self.draw_array(block_arr)
            self.draw_volk()

            if not self.cooldown:
                if self.energy >= 1:
                    if keys[pygame.K_x]:
                        self.energy -= 1
                        pygame.mixer.Sound.play(bullet_sound)
                        all_btn_bullets.append(Bullet(p.usr_x + p.usr_width, p.usr_y + 28))
                        self.cooldown = 60
                    elif click[0]:
                        pygame.mixer.Sound.play(bullet_sound)
                        add_bullet = Bullet(p.usr_x + p.usr_width, p.usr_y + 28)
                        add_bullet.find_path(mouse[0], mouse[1])
                        all_btn_bullets.append(add_bullet)
                        self.cooldown = 60
            else:
                print_text('Time: ' + str(self.cooldown // 10), 20, 150)
                self.cooldown -= 1

            for bullet in all_btn_bullets:
                if not bullet.move():
                    all_btn_bullets.remove(bullet)

            for bullet in all_ms_bullets:
                if not bullet.move_to():
                    all_ms_bullets.remove(bullet)

            heart.move()
            self.heart_plus(heart)

            energ.move()
            self.energ_plus(energ)

            if self.check_collision(block_arr):
                game = False
            self.show_health()
            self.show_energy()

            self.draw_enemy(all_enemies)
            self.check_enemies_dmg(all_btn_bullets, all_enemies)

            pygame.display.update()
            clock.tick(65)

        return self.game_over()

    def jump(self):
        if self.jump_counter >= -30:
            p.usr_y -= self.jump_counter / 2
            self.jump_counter -= 1
        else:
            self.jump_counter = 30
            self.make_jump = False

    def create_block_arr(self, array):
        choice = random.randrange(0, 3)
        img = block_img[choice]
        width = self.block_options[choice * 2]
        height = self.block_options[choice * 2 + 1]
        array.append(Object(display_width + 10, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = block_img[choice]
        width = self.block_options[choice * 2]
        height = self.block_options[choice * 2 + 1]
        array.append(Object(display_width + 300, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = block_img[choice]
        width = self.block_options[choice * 2]
        height = self.block_options[choice * 2 + 1]
        array.append(Object(display_width + 600, height, width, img, 4))

    def object_return(self, objects, obj):
        radius = self.find_radius(objects)

        choice = random.randrange(0, 3)
        img = block_img[choice]
        width = self.block_options[choice * 2]
        height = self.block_options[choice * 2 + 1]

        obj.return_self(radius, height, width, img)

    @staticmethod
    def find_radius(array):
        maximum = max(array[0].x, array[1].x, array[2].x)

        if maximum < display_width:
            radius = display_width
            if radius - maximum < 50:
                radius += 150
        else:
            radius = maximum
        choice = random.randrange(0, 5)
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(200, 350)

        return radius

    def draw_array(self, array):
        for block in array:
            check = block.move()
            if not check:
                self.object_return(array, block)

    def draw_volk(self):
        if self.img_counter == 36:
            self.img_counter = 0
        display.blit(volk_img[self.img_counter // 6], (p.usr_x, p.usr_y))
        self.img_counter += 1

    @staticmethod
    def pause():
        paused = True

        pygame.mixer_music.pause()
        pygame.mixer.Sound.play(pause_sound)
        pygame.mixer.Sound.play(pause_sound, -1)
        pause_sound.set_volume(0.2)

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text0('PAUSE', 320, 30)
            print_text('press ENTER, to continue', 258, 115)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                pygame.mixer_music.unpause()
                pause_sound.set_volume(0)
                paused = False

            pygame.display.update()
            clock.tick(15)

    def check_collision(self, barriers):
        for barrier in barriers:
            if barrier.y >= 0:
                if not self.make_jump:
                    if barrier.x <= p.usr_x + p.usr_width - 80 <= barrier.x + barrier.width:
                        if self.check_health():
                            self.object_return(barriers, barrier)
                            return False
                        else:
                            return True
                elif self.jump_counter == 10:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr_width - 5 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                elif self.jump_counter >= -1:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr_width - 50 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                    else:
                        if p.usr_y + p.usr_height - 5 >= barrier.y:
                            if barrier.x <= p.usr_x + 5 <= barrier.x + barrier.width:
                                if self.check_health():
                                    self.object_return(barriers, barrier)
                                    return False
                                else:
                                    return True
        return False

    def count_scores(self, barriers):
        above_block = 0
        if -20 <= self.jump_counter < 25:
            for barrier in barriers:
                if p.usr_y + p.usr_height - 5 <= barrier.y:
                    if barrier.x <= p.usr_x <= barrier.x + barrier.width:
                        above_block += 1
                    elif barrier.x <= p.usr_x + p.usr_width <= barrier.x + barrier.width:
                        above_block += 1
            self.max_above = max(self.max_above, above_block)
        else:
            if self.jump_counter == -30:
                self.scores += self.max_above
                self.max_above = 0

    def game_over(self):
        pygame.mixer_music.pause()
        pygame.mixer.Sound.play(quit_sound)
        pygame.mixer.Sound.play(quit_sound, -1)
        quit_sound.set_volume(0.2)

        if self.scores > self.max_scores:
            self.max_scores = self.scores

        stopped = True
        while stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text0('GAME OVER', 240, 30)
            print_text('press Enter - to play again', 260, 110)
            print_text('press ESC - to exit', 260, 150)
            print_text('Max score: ' + str(self.max_scores), 260, 190)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                quit_sound.set_volume(0)
                return True
            if keys[pygame.K_ESCAPE]:
                quit_sound.set_volume(0)
                menu_sound.set_volume(0.2)
                return False

            pygame.display.update()
            clock.tick(15)

    def show_health(self):
        show = 0
        x = 10
        while show != self.health:
            display.blit(health_img, (x, 10))
            x += 50
            show += 1

    def check_health(self):
        self.health -= 1
        if self.health == 0:
            return False
        else:
            pygame.mixer.Sound.play(loss_sound)
            loss_sound.set_volume(0.2)
            return True

    def heart_plus(self, heart):
        if p.usr_x <= heart.x <= p.usr_x + p.usr_width:
            if p.usr_y <= heart.y <= p.usr_y + p.usr_height:
                pygame.mixer.Sound.play(heart_sound)
                if self.health <= 2:
                    self.health += 1

                radius = display_width + random.randrange(500, 700)
                heart.return_self(radius, heart.y, heart.width, heart.image)

    def show_energy(self):
        show = 0
        x = 10
        while show != self.energy:
            display.blit(energy_img, (x, 60))
            x += 50
            show += 1

    def energ_plus(self, energ):
        if p.usr_x <= energ.x <= p.usr_x + p.usr_width:
            if p.usr_y <= energ.y <= p.usr_y + p.usr_height:
                pygame.mixer.Sound.play(heart_sound)
                if self.energy <= 2:
                    self.energy += 1

                radius = display_width + random.randrange(100, 800)
                energ.return_self(radius, energ.y, energ.width, energ.image)

    @staticmethod
    def draw_enemy(enemies):
        for enemy in enemies:
            action = enemy.draw()
            if action == 1:
                enemy.show()
            elif action == 2:
                enemy.hide()
            else:
                enemy.shoot()

    @staticmethod
    def check_enemies_dmg(bullets, enemies):
        for enemy in enemies:
            for bullet in bullets:
                enemy.check_dmg(bullet)
