import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
    

        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()

        self.rect = pygame.Rect((x, y, 80, 100))

        # physics
        self.vel_y = 0
        self.running = False
        self.jump = False

        # combat
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.block = False

        # health
        self.health = 100
        self.alive = True


    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size
                )
                temp_img = pygame.transform.scale(
                    temp_img,
                    (self.size * self.image_scale, self.size * self.image_scale)
                )
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list


    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()

        if not self.attacking and self.alive and not round_over:
            #check player controls
            if self.player == 1:
                # movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True

                # jump
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                # attacks
                if key[pygame.K_q] or key[pygame.K_e]:
                    if key[pygame.K_q]: self.attack_type = 1
                    if key[pygame.K_e]: self.attack_type = 2
                    self.attack(target)

                
            #check player controls
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                # jump
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                # attacks
                if key[pygame.K_n] or key[pygame.K_m]:
                    if key[pygame.K_n]: self.attack_type = 1
                    if key[pygame.K_m]: self.attack_type = 2
                    self.attack(target)

               
        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screen_height - 190:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 190 - self.rect.bottom

        # face opponent
        self.flip = target.rect.centerx < self.rect.centerx

        # cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # update pos
        self.rect.x += dx
        self.rect.y += dy


    def update(self):

        # ---------------------------------------------
        # block action commented out since the sprite disappears
        # ---------------------------------------------
        #if self.block:
         #   if self.action != 7:
          #      self.update_action(7)

        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(9)

        elif self.hit:
            self.update_action(8)

        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)

        elif self.jump:
            self.update_action(1)

        elif self.running:
            self.update_action(2)

        else:
            self.update_action(0)

        # animation timing
        ANIMATION_COOLDOWN = 90
        current_time = pygame.time.get_ticks()

        if current_time - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = current_time
            self.frame_index += 1

        # clamp animation BEFORE using frame
        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
                # dead stays on last frame
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.block:
                # block animation freezes at last frame
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

                # attack ends
                if self.action in (3, 4):
                    self.attacking = False
                    self.attack_cooldown = 20

                # hit ends
                if self.action == 8:
                    self.hit = False
                    self.attack_cooldown = 20

        # assign image
        self.image = self.animation_list[self.action][self.frame_index]


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()

            # Correct directional hitbox
            direction = -1 if self.flip else 1

            attacking_rect = pygame.Rect(
                self.rect.centerx + direction * self.rect.width,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )

            # apply damage
            if attacking_rect.colliderect(target.rect) and not target.block:
                target.health -= 10
                target.hit = True

            # debug
            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)

        # debug collision box
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

        # draw sprite
        surface.blit(
            img,
            (
                self.rect.x - (self.offset[0] * self.image_scale),
                self.rect.y - (self.offset[1] * self.image_scale)
            )
        )
