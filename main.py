import sys
import pygame
from src.settings import Settings
from src.engine import GameEnvironment
from src.renderer import Renderer
from src.agent import RandomAgent, HeuristicAgent
from src.llm_parser import LLMParser
from dotenv import load_dotenv

def main():
    load_dotenv()
    settings = Settings()
    engine = GameEnvironment(settings)
    renderer = Renderer(settings)
    agent = HeuristicAgent()
    llm = LLMParser()

    # Get initial observation
    obs = engine._get_observation()
    
    user_text = ""
    input_active = False
    is_ai_playing = True

    running = True
    while running:
        action = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    # Chat Focus Mode
                    if event.key == pygame.K_RETURN:
                        if user_text:
                            updates = llm.parse_command(user_text)
                            if updates:
                                settings.update(updates)
                                print(f"Applied updates: {updates}")
                            user_text = ""
                        input_active = False  # Exit chat
                    elif event.key == pygame.K_ESCAPE:
                        input_active = False  # Cancel chat
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        if event.unicode.isprintable():
                            user_text += event.unicode
                else:
                    # Game Control Mode
                    if event.key == pygame.K_SPACE:
                        if engine.game_over:
                            # Restart the game if dead
                            engine.reset()
                            obs = engine._get_observation()
                        elif not is_ai_playing:
                            # Human jumps if they press Space and AI is off
                            action = 1
                    elif event.key == pygame.K_t:
                        # Toggle Modes
                        is_ai_playing = not is_ai_playing
                    elif event.key == pygame.K_RETURN:
                        # Enter Chat Focus Mode
                        input_active = True
        
        # Agent decides next action (only if playing and not dead)
        if is_ai_playing and not engine.game_over:
            action = agent.predict(obs)
        
        # Step the environment forward
        obs, reward, done, info = engine.step(action=action)
            
        # Draw the frame
        renderer.draw(engine, user_text=user_text, input_active=input_active, is_ai_playing=is_ai_playing)
        renderer.tick()

    renderer.quit()
    sys.exit()

if __name__ == "__main__":
    main()
