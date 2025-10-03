import pygame
from trig import ang_to_cart
from consts import WIDTH, HEIGHT, STEP_TIME, BG_COLOR

class ArmViewer:
    def __init__(self, robot, TAKE, LEAVE, C_MESA_ORIGEN, C_MESA_META, R_MESA, OBSTACLES):
        # Datos
        self.L1 = robot.L1
        self.L2 = robot.L2
        self.instructions_to_take = TAKE
        self.instruction_to_leave = LEAVE
        self.pasos = TAKE + LEAVE

        # Centro de la ventana
        self.cx, self.cy = WIDTH // 2, HEIGHT // 2

        # Config Mesas
        self.c_mesa_origen = C_MESA_ORIGEN
        self.c_mesa_meta = C_MESA_META
        self.r_mesa = R_MESA

        # Config Obstáculo
        self.OBSTACLES = OBSTACLES

        # Animacion
        self.idx = 0
        self.playing = False
        self.t_between = 0.0
        self.carrying_coffee = False

        pygame.init()
        pygame.display.set_caption("Brazo 2-DoF")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)

    def reset(self):
        self.idx = 0
        self.playing = False
        self.t_between = 0.0
        self.carrying_coffee = False
        self.coffe_position = self.c_mesa_origen

    def draw_axes(self):
        pygame.draw.line(self.screen, (200, 200, 200), (0, self.cy), (WIDTH, self.cy), 1)
        pygame.draw.line(self.screen, (200, 200, 200), (self.cx, 0), (self.cx, HEIGHT), 1)

    def draw_tables(self):
        pygame.draw.circle(self.screen, (150, 75, 0), (self.cx + self.c_mesa_origen[0], self.cy - self.c_mesa_origen[1]), self.r_mesa)
        pygame.draw.circle(self.screen, (150, 75, 0), (self.cx + self.c_mesa_meta[0], self.cy - self.c_mesa_meta[1]), self.r_mesa)

    def draw_goal(self):
        gx, gy = self.meta
        p = (self.cx + int(gx), self.cy - int(gy)) 
        pygame.draw.circle(self.screen, (0, 180, 0), p, 8)

    def draw_coffee(self):
        pos_x, pos_y = self.coffe_position
        taza_radio = 8
        cafe_radio = 5

        pygame.draw.circle(self.screen, (120, 120, 120), (self.cx + pos_x, self.cy - pos_y), taza_radio, 3)
        pygame.draw.circle(self.screen, (150, 75, 0), (self.cx + pos_x, self.cy - pos_y), cafe_radio, 0)

    def draw_max_radius(self):
        pygame.draw.circle(self.screen, (200, 200, 200), (self.cx, self.cy), self.L1 + self.L2, 1)
        pygame.draw.circle(self.screen, (200, 200, 200), (self.cx, self.cy), abs(self.L1 - self.L2), 1)

    def draw_arm(self, theta1, theta2):
        (x1, y1), (x2, y2) = ang_to_cart(theta1, theta2, self.L1, self.L2)
        # print((x1, y1), (x2, y2))

        # convertir coords relativas al centro de la pantalla
        base = (self.cx, self.cy)
        brazo_1 = (self.cx + int(x1), self.cy - int(y1))
        brazo_2 = (self.cx + int(x2), self.cy - int(y2))

        if self.carrying_coffee == True:
            self.coffe_position = (x2, y2)
        
        # Brazo
        pygame.draw.line(self.screen, (0, 0, 255), base, brazo_1, 5)
        pygame.draw.line(self.screen, (255, 0, 0), brazo_1, brazo_2, 5)

        # Articulaciones
        pygame.draw.circle(self.screen, (0, 0, 0), base, 5)
        pygame.draw.circle(self.screen, (0, 0, 0), brazo_1, 5)
        pygame.draw.circle(self.screen, (0, 0, 0), brazo_2, 5)

    def draw_obstacles(self):
        for ob in self.OBSTACLES:
            ob.draw(self.screen)

    def draw_hud(self, theta1, theta2):
        lines = [
            "[ESPACIO] Play/Pause   [←/→] Atras/Adelante   [R] Reset   [ESC] Salir",
            f"Paso: {self.idx+1}/{len(self.pasos)}",
            f"θ1: {theta1:+.2f} rad   θ2: {theta2:+.2f} rad",
        ]
        y = 10
        for line in lines:
            surf = self.font.render(line, True, (20, 20, 20))
            self.screen.blit(surf, (10, y))
            y += 20

    def current_angles(self):
        return self.pasos[self.idx]

    def update_play(self, dt):
        if not self.playing:
            return
        self.t_between += dt
        if self.t_between >= STEP_TIME:
            self.t_between = 0.0
            if self.idx < len(self.pasos) - 1:
                self.idx += 1
            else:
                self.playing = False

    def step_forward(self):
        if self.idx < len(self.pasos) - 1:
            self.idx += 1
        self.t_between = 0.0
        self.playing = False

    def step_backward(self):
        if self.idx > 0:
            self.idx -= 1
        self.t_between = 0.0
        self.playing = False

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        if self.idx >= len(self.pasos) - 1 and not self.playing:
                            self.reset()
                        self.playing = not self.playing
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_RIGHT:
                        self.step_forward()
                    elif event.key == pygame.K_LEFT:
                        self.step_backward()

            self.update_play(dt)
            theta1, theta2 = self.current_angles()

            #if self.idx >= len(self.instructions_to_take):
            #    self.carrying_coffee = True

            self.screen.fill(BG_COLOR)
            self.draw_axes()
            self.draw_tables()
            self.draw_max_radius()
            self.draw_arm(theta1, theta2)
            self.draw_hud(theta1, theta2)
            self.draw_obstacles()
            #self.draw_coffee()

            pygame.display.flip()

        pygame.quit()
