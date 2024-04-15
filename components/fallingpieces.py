import pygame

from config.settings import WINDOW_HEIGHT


class FallingSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, speed, rotate_speed) -> None:
        self.original_image = image  # Store the original image for reference
        self.image = image.copy()  # Create a working copy for rotation
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed_y = speed
        self.angle = 0
        self.rotate_speed = rotate_speed

    def update(self, dt: float) -> None:
        self.rect.y += self.speed_y * dt

        # Calculate half width and half height
        half_width = self.image.get_rect().width // 2
        half_height = self.image.get_rect().height // 2

        # Calculate maximum corner distance from center (diagonal)
        max_distance = (half_width**2 + half_height**2) ** 0.5

        # Calculate rotation speed based on desired speed and max distance
        self.angle += (self.rotate_speed) / max_distance

        # Rotate the working copy of the image using smoothscale
        # This is where the performance hit happens.
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Check for screen bottom and reset (optional)
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0
