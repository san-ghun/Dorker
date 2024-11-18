import os

# Fill in the directory name that contains all your 42 projects
DORKER_WORKSPACE = os.path.join(os.environ['HOME'], 'Projects/42berlin')
DORKER_ECHO_ON_STARTUP = True

# ANSI color codes
class Colors:
    GREEN = '\033[0;32m'  # Success messages
    BLUE = '\033[0;36m'   # Instructions/guides
    RED = '\033[0;31m'    # Errors/warnings
    WHITE = '\033[0m'     # Reset color 