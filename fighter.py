import pygame
class Fighter():
    def __init__(self, x,y,flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0: idle #1:jump #2 run #3 attack1 #4 attack2 #5 block #6 getHit #7 getlauched #8 death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x,y,80,100))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    def load_images(self, sprite_sheet, animation_steps):
        #get images for sprites
        #sprite_sheet = pygame.image.load(sprite_sheet)
        animation_list = []
        for y,animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
                
            animation_list.append(temp_img_list)
        return animation_list

    def move(self,screen_width,screen_height,surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0



        #get key pressses
        key = pygame.key.get_pressed()

        
        #can only perform other actions is not attacking
        if self.attacking == False:

        #movment
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
            if key[pygame.K_d]:
                dx = SPEED
                self.running = True
            #jump
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            
            #attack 
            #work similar to smash each button press is a different attack in the combo
            if key[pygame.K_q] or key[pygame.K_e]:
                self.attack(surface,target)

                #determine which attck
                #melee attack
                if key[pygame.K_q]:
                    self.attack_type = 1
                #ranged attack
                if key[pygame.K_e]:
                    self.attack_type = 2
        #applies gravity
        self.vel_y+= GRAVITY
        dy += self.vel_y



        #ensures fighter stays in screen
        if self.rect.left +dx < 0:
            dx = - self.rect.left
        if self.rect.right +dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height -190:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 190 - self.rect.bottom
        
        #ensure player face each other
        if(target.rect.centerx> self.rect.centerx):
            self.flip = False
        else:
            self.flip = True

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    #animation update
    def update(self):
        #check to see what action is happening
        if self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
            self.attacking = False
        elif self.jump:
            self.update_action(1)
        elif self.running:
            self.update_action(2)
        else:
            self.update_action(0)

        
        cooldown = 95
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.frame_index+=1
            self.update_time = pygame.time.get_ticks()
        #check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


    #checking if the new action is different from previous
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            # Reset animation only if the action changes
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def attack(self, surface, target ):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y, 1 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        pygame.draw.rect(surface, (0,255,0), attacking_rect)

    def draw(self,surface):
        img = pygame.transform.flip(self.image, self.flip,False)
        pygame.draw.rect(surface, (255,0,0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))




