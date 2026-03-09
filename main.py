import sys
import pygame
from src.settings import Settings
from src.engine import GameEnvironment
from src.renderer import Renderer
from src.agent import RandomAgent, HeuristicAgent
from src.llm_parser import LLMParser

def main():
    settings = Settings()
    engine = GameEnvironment(settings)
    renderer = Renderer(settings)
    agent = HeuristicAgent()
    llm = LLMParser()

    # Get initial observation
    obs = engine._get_observation()
    
    user_text = ""
    input_active = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and engine.game_over:
                    # Space ONLY restarts if game over, to allow typing spaces normally
                    engine.reset()
                    obs = engine._get_observation()
                elif input_active:
                    if event.key == pygame.K_RETURN:
                        # Send text to Layer 3!
                        if user_text:
                            updates = llm.parse_command(user_text)
                            if updates:
                                settings.update(updates)
                                print(f"Applied updates: {updates}")
                            user_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        # Only allow basic typing if not escaping or doing weird commands
                        if event.unicode.isprintable():
                            user_text += event.unicode
        
        # Agent decides next action based on previous observation
        action = 0
        if not engine.game_over:
            action = agent.predict(obs)
        
        # Step the environment forward based on Agent's action
        obs, reward, done, info = engine.step(action=action)
            
        # Decoupled Draw tick
        renderer.draw(engine, user_text=user_text, input_active=input_active)
        renderer.tick()

    renderer.quit()
    sys.exit()

if __name__ == "__main__":
    main()
