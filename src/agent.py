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
