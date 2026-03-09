import sys
import pygame
from src.settings import Settings
from src.engine import GameEnvironment
from src.renderer import Renderer

def main():
    settings = Settings()
    engine = GameEnvironment(settings)
    renderer = Renderer(settings)

    running = True
    while running:
        action = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if engine.game_over:
                        engine.reset()
                    else:
                        action = 1
        
        # Decoupled Engine tick
        engine.update(action=action)
            
        # Decoupled Draw tick
        renderer.draw(engine)
        renderer.tick()

    renderer.quit()
    sys.exit()

if __name__ == "__main__":
    main()
