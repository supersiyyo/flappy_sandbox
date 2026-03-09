God Mode AI Sandbox: Flappy Bird Edition
🎯 Project Overview

This repository contains a strictly decoupled, modular clone of "Flappy Bird" built in Python using Pygame. The objective is to create a live, interactive physics sandbox.

    An AI agent (e.g., NEAT or RL) will continuously play the game.

    The user acts as the "Game Director," using a natural language text prompt to alter the game's physics and rules in real-time while the AI is playing.

🏗️ Core Architectural Philosophy (Layered Design)

DO NOT DEVIATE FROM THIS PATTERN.
This project strictly enforces the separation of concerns across three layers:

    Layer 1: The Game Engine (Physics & Rendering)

        The game state (gravity, bird velocity, pipe speed, pipe movement) must exist entirely independent of the visual rendering.

        All physics variables must be stored in a dynamic, easily mutable configuration state (src/settings.py).

    Layer 2: The AI Player (The Agent)

        The game must package its state into a discrete "Observation" array [bird_y, velocity, dist_to_pipe, pipe_gap_y].

        The game must accept binary "Actions" (1 for Jump, 0 for Do Nothing) via an AgentController interface.

    Layer 3: The Command Center (LLM Prompt Parser)

        A text input interface where the user types commands (e.g., "Make gravity 2X heavier").

        This text is parsed by an LLM to output a JSON string of variable updates, instantly mutating Layer 1 without restarting the game loop.

📁 Required Project Structure

To maintain strict decoupling, the codebase must adhere to the following structure:
flappy_sandbox/
├── README.md
├── main.py              # Entry point to initialize the engine
└── src/
├── settings.py      # Mutable Config class/dict for all physics/rules
├── entities.py      # Bird and Pipe classes (pygame.sprite.Sprite)
├── engine.py        # GameEnvironment class (Physics math ONLY)
└── renderer.py      # Pygame drawing and display logic ONLY

## 🚀 Setup & Run Instructions

To run the sandbox locally, you must use a Python virtual environment to avoid system package conflicts.

1. Ensure Python 3.10+ is installed on your system.
2. Initialize and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the engine dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the decoupled game engine loop:
   ```bash
   python main.py
   ```

🗺️ Agentic Iteration Roadmap

INSTRUCTIONS FOR AI DEVELOPERS: Execute this plan iteratively. Do not attempt to build multiple phases at once. Complete a phase, provide the code, and wait for human verification before proceeding.
Phase 1: The Baseline Engine (Current Objective)

    [ ] Initialize Python environment and folder structure exactly as outlined above.

    [ ] Create src/settings.py containing the mutable configuration.

    [ ] Build src/entities.py utilizing precise bounding-box collisions.

    [ ] Build src/engine.py with an update() method that advances physics by one frame.

    [ ] Build src/renderer.py to handle the visual translation to the Pygame display.

    STOP AND WAIT FOR HUMAN APPROVAL.

Phase 2: Agent Interface (Layer 2)

    [ ] Standardize the step(action) method in the engine to return (observation, reward, done, info).

    [ ] Hook up a baseline random agent or placeholder RL model to test autonomous play.

    STOP AND WAIT FOR HUMAN APPROVAL.

Phase 3: The Command Center (Layer 3)

    [ ] Build the UI overlay for the text input box ("Modify the game...").

    [ ] Integrate a lightweight LLM API tool to map natural language strings to settings.py JSON overrides.

    [ ] Ensure the game loop can handle mid-run physics changes without crashing.
