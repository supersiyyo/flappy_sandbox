import random

class RandomAgent:
    """A baseline AI Agent that randomly decides to flap or do nothing."""
    def __init__(self):
        pass

    def predict(self, observation):
        """
        Takes in the environment observation and returns an action.
        Observation format: [bird_y, bird_velocity, dist_to_next_pipe, next_pipe_gap_y]
        Action format: 1 (Jump) or 0 (Do Nothing)
        """
        # A simple random policy: 10% chance to flap every frame
        # We can ignore the observation because it's random
        if random.random() < 0.10:
            return 1
        return 0

class HeuristicAgent:
    """A hardcoded AI that calculates when to flap based on exact observation values."""
    def __init__(self):
        pass

    def predict(self, observation):
        """
        Takes in the environment observation and returns an action.
        Observation format: [bird_y, bird_velocity, dist_to_next_pipe, next_pipe_gap_y]
        Action format: 1 (Jump) or 0 (Do Nothing)
        """
        bird_y, bird_velocity, dist_to_next_pipe, next_pipe_gap_y = observation
        
        # Target the center of the gap (assuming gap is ~150px)
        # Using 60 so it aims slightly above the exact center
        target_y = next_pipe_gap_y + 60
        
        # If the bird is below the target and falling (or about to fall too far), flap!
        # Remember: higher y value means lower on the screen
        if bird_y > target_y and bird_velocity > -3:
            return 1
            
        return 0
