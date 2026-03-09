import sys
import pygame
from src.settings import Settings
from src.engine import GameEnvironment
from src.renderer import Renderer
from src.agent import RandomAgent

def main():
    settings = Settings()
    engine = GameEnvironment(settings)
    renderer = Renderer(settings)
    agent = RandomAgent()

    # Get initial observation
    obs = engine._get_observation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if engine.game_over:
                        engine.reset()
                        obs = engine._get_observation()
        
        # Agent decides next action based on previous observation
        action = 0
        if not engine.game_over:
            action = agent.predict(obs)
        
        # Step the environment forward based on Agent's action
        obs, reward, done, info = engine.step(action=action)
            
        # Decoupled Draw tick
        renderer.draw(engine)
        renderer.tick()

    renderer.quit()
    sys.exit()

if __name__ == "__main__":
    main()
