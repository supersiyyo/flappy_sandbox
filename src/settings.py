class Settings:
    def __init__(self):
        # Display settings
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        
        # Physics settings
        self.GRAVITY = 0.5
        self.FLAP_STRENGTH = -8.0
        self.MAX_VELOCITY = 10.0
        
        # Pipe settings
        self.PIPE_SPEED = 3.0
        self.PIPE_WIDTH = 60
        self.PIPE_GAP_SIZE = 150
        self.PIPE_SPAWN_FREQUENCY = 100 # In frames
        
        # Bird settings
        self.BIRD_X = 100
        self.BIRD_WIDTH = 30
        self.BIRD_HEIGHT = 30
        
        # Aesthetic settings (Mutable via LLM)
        self.BG_COLOR = (135, 206, 235)       # Sky blue
        self.BIRD_COLOR = (255, 215, 0)       # Gold/Yellow
        self.PIPE_COLOR = (34, 139, 34)       # Forest green
        self.TEXT_COLOR = (255, 255, 255)     # White

    def update(self, config_updates: dict):
        """Allows dynamically updating the physics configuration mid-game."""
        for key, value in config_updates.items():
            if hasattr(self, key):
                setattr(self, key, type(getattr(self, key))(value))
