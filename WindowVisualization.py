import pygame as pg



class WindowVisualization:
    def __init__(
            self, width: int = 1280,
            height: int = 720,
            fps: int = 30,
            player_radius: int = 1,
        ) -> None:
        
        pg.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.player_radius = player_radius


        self.window = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

        pg.display.set_caption("Simulation Visualization")


    def run_frame(self, points: dict[int, tuple[tuple[float, float], tuple[int, int, int]]]) -> None:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        self.window.fill((255, 255, 255))

        for playerId, (position, color) in points.items():
            pg.draw.circle(self.window, color, (position[0], position[1]), self.player_radius)

        pg.display.update()
        self.clock.tick(self.fps)

    def quit_window(self) -> None:
        pg.quit()