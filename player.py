import os

import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface,create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust
        self.import_dust_particles_running()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.touching_ground = False
        self.touching_ceiling = False
        self.touching_left = False
        self.touching_right = False

    def import_character_assets(self):
        character_path = r'.\graphics\character'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + "\\" + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_particles_running(self):
        self.dust_particles_running = import_folder(r'.\graphics\character\dust_particles\run')

    def animate(self):
        animation = self.animations[self.status]

        #
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image,True,False)

        # setting rect to put player on surface
        if self.touching_ground and self.touching_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.touching_ground and self.touching_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.touching_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.touching_ceiling and self.touching_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.touching_ceiling and self.touching_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.touching_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        # else:
        #   self.rect = self.image.get_rect(center = self.rect.center)

    def dust_animate(self):
        if self.status == 'run' and self.touching_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_particles_running):
                self.dust_frame_index = 0
            dust_particle = self.dust_particles_running[int(self.dust_frame_index)]
            if self.facing_right:
                self.display_surface.blit(dust_particle,self.rect.bottomleft - pygame.math.Vector2(10,10))
            else:
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,self.rect.bottomright - pygame.math.Vector2(10,10))

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.touching_ground:
            self.frame_index = 0
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0.81:  # y>0 - messud up glitch based on collision problem -> raised from 0 to anything > gravity
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.dust_animate()

