import os
from src.settings import Colors, DORKER_ECHO_ON_STARTUP
from src import docker, dorker

def initialize():
    """Initialize dorker environment"""
    # Import all necessary modules
    if DORKER_ECHO_ON_STARTUP:
        print(f"{Colors.GREEN}Dorker commands successfully loaded{Colors.WHITE}")

if __name__ == "__main__":
    initialize() 