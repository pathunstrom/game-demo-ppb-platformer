import ppb
import ppb.keycodes

class Player(ppb.Sprite):
    jump_velocity: ppb.Vector = ppb.Vector(0, 0)
    grounded = False
    intent = ppb.Vector(0, 0)
    speed = 4
    size = 0.99

    def on_update(self, event: ppb.events.Update, signal: ppb.Signal):
        if self.intent:
            self.position += self.intent.normalize() * self.speed * event.time_delta
        self.position += self.jump_velocity * event.time_delta
        self.jump_velocity += ppb.directions.Down * 9.5 * event.time_delta
        self.grounded = False
        for platform in event.scene.get(tag="platforms"):
            if platform.in_surface(self):
                self.bottom = platform.top
                self.grounded = True
            elif platform.in_bottom(self):
                self.top = platform.bottom
                self.jump_velocity = ppb.Vector(0, -1)
            elif platform.in_left(self):
                self.right = platform.left
            elif platform.in_right(self):
                self.left = platform.right
        if self.grounded:
            self.jump_velocity = ppb.Vector(0, 0)

    def on_key_pressed(self, event: ppb.events.KeyPressed, signal: ppb.Signal):
        if event.key is ppb.keycodes.A:
            self.intent += ppb.directions.Left
        elif event.key is ppb.keycodes.D:
            self.intent += ppb.directions.Right
        elif event.key is ppb.keycodes.Space and self.grounded:
            self.jump_velocity = ppb.directions.Up * 9

    def on_key_released(self, event: ppb.events.KeyReleased, signal: ppb.Signal):
        if event.key is ppb.keycodes.A:
            self.intent -= ppb.directions.Left
        elif event.key is ppb.keycodes.D:
            self.intent -= ppb.directions.Right

    def reset(self):
        self.position = ppb.Vector(0, 0)
        self.intent = ppb.Vector(0, 0)
        self.jump_velocity = ppb.Vector(0, 0)


class Platform(ppb.RectangleSprite):
    image = ppb.Rectangle(200, 100, 100, (3, 1))
    top_surface: 'PlatformCollider'
    bottom_surface: 'PlatformCollider'
    left_wall: 'WallCollider'
    right_wall: 'WallCollider'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_surface = PlatformCollider(width=self.width, height=0.25)
        self.top_surface.top = self.top
        self.bottom_surface = PlatformCollider(width=self.width, height=0.25)
        self.bottom_surface.bottom = self.bottom
        self.right_wall = WallCollider(width=0.25, height=self.height)
        self.right_wall.right = self.right
        self.left_wall = WallCollider(width=0.25, height=self.height)
        self.left_wall.left = self.left

    def in_left(self, sprite: ppb.Sprite):
        return self.left_wall.left <= sprite.right <= self.left_wall.right and not (sprite.top <= self.bottom or sprite.bottom >= self.top)

    def in_right(self, sprite: ppb.Sprite):
        return self.right_wall.right >= sprite.left >= self.right_wall.left and not (sprite.top <= self.bottom or sprite.bottom >= self.top)

    def in_surface(self, sprite: ppb.Sprite):
        return self.top_surface.top >= sprite.bottom >= self.top_surface.bottom and not (sprite.right <= self.left or sprite.left >= self.right)

    def in_bottom(self, sprite: ppb.Sprite):
        return self.bottom_surface.bottom <= sprite.top <= self.bottom_surface.top and not (sprite.right <= self.left or sprite.left >= self.right)


class WallCollider(ppb.RectangleSprite):
    image = None


class PlatformCollider(ppb.RectangleSprite):
    image = None


class Game(ppb.Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(Player(), tags=["player"])
        platforms = [
            Platform(width=3, height=1, position=ppb.Vector(0, -5)),
            Platform(width=3, height=1, position=ppb.Vector(2, -3)),
            Platform(width=3, height=1, position=ppb.Vector(-3, -4)),
        ]
        for platform in platforms:
            self.add(platform, tags=["platforms"])

    def on_key_pressed(self, event: ppb.events.KeyPressed, signal: ppb.Signal):
        if event.key is ppb.keycodes.Escape:
            for player in self.get(tag="player"):
                player.reset()


ppb.run(starting_scene=Game)
