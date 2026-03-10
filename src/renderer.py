import pygame

class Renderer:
    """Handles Pygame drawing and display logic ONLY."""
    def __init__(self, settings):
        self.settings = settings
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption("God Mode AI Sandbox: Flappy Bird Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, engine, user_text="", input_active=True, is_ai_playing=True):
        """Takes engine state and draws it entirely visually."""
        self.screen.fill(self.settings.BG_COLOR)

        # Draw pipes
        for pipe in engine.pipes:
            pygame.draw.rect(self.screen, self.settings.PIPE_COLOR, pipe.top_rect)
            pygame.draw.rect(self.screen, self.settings.PIPE_COLOR, pipe.bottom_rect)
            
        # Draw bird
        pygame.draw.rect(self.screen, self.settings.BIRD_COLOR, engine.bird.rect)
        
        # UI overlays
        if not engine.game_over:
            score_surf = self.font.render(f"Score: {engine.score}", True, self.settings.TEXT_COLOR)
            self.screen.blit(score_surf, (10, 10))
            
            # Active Player Overlay
            mode_text = "[T] Mode: AI Agent" if is_ai_playing else "[T] Mode: Human (Spacebar)"
            mode_color = (255, 100, 100) if is_ai_playing else (100, 255, 100)
            mode_surf = self.font.render(mode_text, True, mode_color)
            self.screen.blit(mode_surf, (self.settings.SCREEN_WIDTH - mode_surf.get_width() - 10, 10))
        else:
            game_over_surf = self.font.render("Game Over! Space to Restart", True, (255, 0, 0))
            text_rect = game_over_surf.get_rect(center=(self.settings.SCREEN_WIDTH//2, self.settings.SCREEN_HEIGHT//2 - 50))
            self.screen.blit(game_over_surf, text_rect)

        # Draw Text Input Overlay
        input_box = pygame.Rect(10, self.settings.SCREEN_HEIGHT - 50, self.settings.SCREEN_WIDTH - 20, 40)
        pygame.draw.rect(self.screen, (255, 255, 255) if input_active else (200, 200, 200), input_box)
        pygame.draw.rect(self.screen, (255, 0, 0) if input_active else (100, 100, 100), input_box, 2) # Border
        
        prompt_text = "Dir:" if input_active else "[ENTER] command:"
        prompt_surf = self.font.render(prompt_text, True, (0, 0, 0) if input_active else (100, 100, 100))
        self.screen.blit(prompt_surf, (input_box.x + 5, input_box.y + 8))
        
        display_text = user_text if input_active else (user_text or "...")
        txt_surf = self.font.render(display_text, True, (0, 0, 0) if input_active else (100, 100, 100))
        
        # Handle text overflow visually
        text_rect_width = max(input_box.w - prompt_surf.get_width() - 15, 10)
        self.screen.set_clip(pygame.Rect(input_box.x + prompt_surf.get_width() + 10, input_box.y, text_rect_width, input_box.h))
        self.screen.blit(txt_surf, (input_box.x + prompt_surf.get_width() + 10, input_box.y + 8))
        self.screen.set_clip(None)

        pygame.display.flip()
        
    def tick(self):
        """Regulate frame rate based on settings."""
        self.clock.tick(self.settings.FPS)

    def quit(self):
        """Closes renderer."""
        pygame.quit()
