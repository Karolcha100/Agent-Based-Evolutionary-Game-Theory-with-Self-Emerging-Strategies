import pygame as pg



class WindowVisualization:
    def __init__(self, width : int = 1280,
                height : int = 720,
                fps : int = 30,
                scaler : int = 4) -> None:
        
        pg.init()
        self.width = width*scaler
        self.height = height*scaler
        self.fps = fps
        self.scaler = scaler

        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Simulation Visualization")
        self.clock = pg.time.Clock()

    def run(self, points: dict[int, tuple[tuple[float, float], tuple[int, int, int]]], 
            playerRadius: int = 1) -> None:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        self.window.fill((255, 255, 255))

        for playerId, (position, color) in points.items():
            pg.draw.circle(self.window, color, (position[0]*self.scaler, position[1]*self.scaler), playerRadius)

        pg.display.update()
        self.clock.tick(self.fps)

    def quitWindow(self) -> None:
        pg.quit()