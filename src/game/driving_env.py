import pygame
import random
import os

PIXELS_PER_METER = 10
CAR_LENGTH_M = 4
CAR_WIDTH_M = 2.2

CAR_HEIGHT_PX = int(CAR_LENGTH_M * PIXELS_PER_METER * 1.4)
CAR_WIDTH_PX = int(CAR_WIDTH_M * PIXELS_PER_METER * 1.4)

NUM_LANES = 3
LANE_WIDTH_M = 3.5
SCREEN_METERS_WIDE = NUM_LANES * LANE_WIDTH_M + 6

ASSET_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')


class DrivingEnv:
    def __init__(self, screen):
        self.screen = screen
        self.coins_collected = 0

        self.screen_width, self.screen_height = self.screen.get_size()
        self.meters_per_pixel = SCREEN_METERS_WIDE / self.screen_width
        self.pixels_per_meter = 1 / self.meters_per_pixel

        self.road_width = NUM_LANES * LANE_WIDTH_M * self.pixels_per_meter
        self.road_left = (self.screen_width - self.road_width) // 2

        # Load images
        self.player_img = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_DIR, 'player_car.png')),
            (CAR_WIDTH_PX, CAR_HEIGHT_PX))
        self.car_img = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_DIR, 'obstacle_car.png')),
            (CAR_WIDTH_PX, CAR_HEIGHT_PX))
        self.coin_img = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_DIR, 'coin.png')), (35, 35))
        self.fuel_img = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_DIR, 'fuel.png')), (35, 35))

        # Load sounds
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.crash_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'crash.wav'))
        self.coin_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'coin.wav'))
        self.fuel_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, 'fuel.wav'))

        # ✅ Play background road noise continuously
        pygame.mixer.music.load(os.path.join(ASSET_DIR, 'road.wav'))
        pygame.mixer.music.set_volume(0.5)  # Optional: adjust volume
        pygame.mixer.music.play(loops=-1)

        self.reset()

    def reset(self):
        self.coins_collected = 0  # Reset coins

        self.speed_increase_timer = 0
        lane_px = LANE_WIDTH_M * self.pixels_per_meter
        self.lane_positions = [
            self.road_left + i * lane_px + (lane_px // 2 - CAR_WIDTH_PX // 2)
            for i in range(NUM_LANES)]
        self.current_lane = 1
        self.player_x = self.lane_positions[self.current_lane]
        self.player_y = self.screen_height - CAR_HEIGHT_PX - 20

        self.speed = 30
        self.fuel = 100
        self.distance = 0
        self.obstacles = []
        self.pickups = []
        self.spawn_timer = 0
        self.lane_switch_cooldown = 0

    def switch_lane(self, direction):
        if direction == 'left' and self.current_lane > 0:
            self.current_lane -= 1
        elif direction == 'right' and self.current_lane < NUM_LANES - 1:
            self.current_lane += 1

    def spawn_obstacle(self):
        lane = random.randint(0, NUM_LANES - 1)
        x = self.lane_positions[lane]
        y = -CAR_HEIGHT_PX
        self.obstacles.append({'img': self.car_img, 'x': x, 'y': y, 'lane': lane})

        if random.random() < 0.5:
            near_lane = max(0, min(NUM_LANES - 1, lane + random.choice([-1, 1])))
            cx = self.lane_positions[near_lane] + 10
            self.pickups.append({'type': 'coin', 'img': self.coin_img, 'x': cx, 'y': y + 40})

        if random.random() < 0.2:
            fx = self.lane_positions[random.randint(0, NUM_LANES - 1)] + 10
            self.pickups.append({'type': 'fuel', 'img': self.fuel_img, 'x': fx, 'y': y + 60})

    def update(self, keys):
        if self.lane_switch_cooldown > 0:
            self.lane_switch_cooldown -= 1

        command = None
        if keys[pygame.K_LEFT]:
            command = 'take left'
        elif keys[pygame.K_RIGHT]:
            command = 'take right'
        elif keys[pygame.K_UP]:
            command = 'accelerate'
        elif keys[pygame.K_DOWN]:
            command = 'stop'

    # Apply control logic
        if command == 'take left' and self.lane_switch_cooldown == 0:
            self.switch_lane('left')
            self.lane_switch_cooldown = 10
        elif command == 'take right' and self.lane_switch_cooldown == 0:
            self.switch_lane('right')
            self.lane_switch_cooldown = 10

        if command == 'accelerate':
            self.speed = min(self.speed + 1, 150)
            self.player_y = max(self.player_y - 2, 100)
        if command == 'stop':
            if self.speed > 0:
                self.speed -= 1
            elif self.speed < 0:
                self.speed += 1
            self.player_y = min(self.player_y + 2, self.screen_height - CAR_HEIGHT_PX - 10)

        target_x = self.lane_positions[self.current_lane]
        self.player_x += (target_x - self.player_x) * 0.2

        meters_moved = 0.1 + (self.speed * 0.004)
        self.distance += meters_moved
        self.fuel -= abs(meters_moved) * 0.2

        if self.fuel <= 0:
            self.crash_sound.play()
            return True

        for obs in self.obstacles:
            obs['y'] += meters_moved * self.pixels_per_meter
        for pickup in self.pickups:
            pickup['y'] += meters_moved * self.pixels_per_meter

        self.obstacles = [o for o in self.obstacles if o['y'] < self.screen_height]
        self.pickups = [p for p in self.pickups if p['y'] < self.screen_height]

        self.spawn_timer += 1
        if self.spawn_timer > 80:
            self.spawn_obstacle()
            self.spawn_timer = 0

        player_rect = pygame.Rect(self.player_x, self.player_y, CAR_WIDTH_PX, CAR_HEIGHT_PX)
        for obs in self.obstacles:
            obs_rect = pygame.Rect(obs['x'], obs['y'], CAR_WIDTH_PX, CAR_HEIGHT_PX)
            if player_rect.colliderect(obs_rect):
                self.crash_sound.play()
                return True

        for pickup in self.pickups[:]:
            pickup_rect = pygame.Rect(pickup['x'], pickup['y'], 30, 30)
            if player_rect.colliderect(pickup_rect):
                if pickup['type'] == 'coin':
                    self.coins_collected += 1
                    self.coin_sound.play()
                elif pickup['type'] == 'fuel':
                    self.fuel = min(100, self.fuel + 30)
                    self.fuel_sound.play()
                self.pickups.remove(pickup)

        self.speed_increase_timer += 1
        if self.speed_increase_timer >= 400:
            self.speed = min(self.speed + 1, 150)
            self.speed_increase_timer = 0

        return False


    def draw_road(self):
        pygame.draw.rect(self.screen, (45, 45, 45), (self.road_left, 0, self.road_width, self.screen_height))

        lane_line_x = LANE_WIDTH_M * self.pixels_per_meter
        dash_length = 20
        gap_length = 20

        if not hasattr(self, 'dash_offset'):
            self.dash_offset = 0
        self.dash_offset -= self.speed * 0.2
        self.dash_offset %= (dash_length + gap_length)

        for i in range(1, NUM_LANES):
            x = self.road_left + i * lane_line_x
            y = -self.dash_offset
            while y < self.screen_height:
                pygame.draw.line(self.screen, (220, 220, 220), (x, y), (x, y + dash_length), 3)
                y += dash_length + gap_length

        pygame.draw.line(self.screen, (200, 200, 200), (self.road_left, 0), (self.road_left, self.screen_height), 4)
        pygame.draw.line(self.screen, (200, 200, 200), (self.road_left + self.road_width, 0),
                         (self.road_left + self.road_width, self.screen_height), 4)

    def render(self):
        self.screen.fill((0, 150, 0))
        self.draw_road()
        self.screen.blit(self.player_img, (self.player_x, self.player_y))
        for obs in self.obstacles:
            self.screen.blit(obs['img'], (obs['x'], obs['y']))
        for pickup in self.pickups:
            self.screen.blit(pickup['img'], (pickup['x'], pickup['y']))

        hud_rect = pygame.Rect(10, 10, 250, 140)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), hud_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), hud_rect, 2)
        self.screen.blit(self.font.render(f"Speed: {int(self.speed)} km/h", True, (255, 255, 255)), (20, 20))
        self.screen.blit(self.font.render(f"Distance: {int(self.distance)} m", True, (255, 255, 255)), (20, 50))
        self.screen.blit(self.font.render(f"Fuel: {int(self.fuel)}%", True, (255, 255, 255)), (20, 80))
        self.screen.blit(self.font.render(f"Coins: {self.coins_collected}", True, (255, 255, 255)), (20, 110))
        # self.screen.blit(self.font.render("Press Q to Quit", True, (200, 200, 200)), (20, 140))

    