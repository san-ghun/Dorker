import os
import subprocess
from pathlib import Path
from .settings import DORKER_WORKSPACE, Colors

def check_environment():
    """Check if current directory is within workspace and docker is running properly"""
    current_path = Path.cwd()
    workspace_path = Path(DORKER_WORKSPACE)
    
    # Check if current directory is in workspace
    if not any(parent == workspace_path for parent in current_path.parents):
        print(f"{Colors.RED}You are not inside the workspace specified.{Colors.WHITE}")
        print(f"{Colors.BLUE}Dorker can only be ran inside the specified workspace, "
              f"currently it is set to \"{DORKER_WORKSPACE}\". "
              f"To change it, please modify src/settings.py{Colors.WHITE}")
        return False
    
    # Check if dorker container is running
    try:
        result = subprocess.run(
            ['docker', 'ps'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        if 'dorker' not in result.stdout:
            # Check if dorker image exists
            image_result = subprocess.run(
                ['docker', 'images', '-q', 'dorker'],
                capture_output=True,
                text=True,
                check=True
            )
            if not image_result.stdout.strip():
                init_dorker()
            else:
                # Run the container if image exists
                subprocess.run([
                    'docker', 'run', '-itd',
                    '-p', '8080:8080',
                    '-v', f'{DORKER_WORKSPACE}:/dorker_workspace',
                    '--name=dorker',
                    'dorker'
                ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Docker command failed: {e}{Colors.WHITE}")
        return False
    
    return True

def init_dorker():
    """Initialize dorker image and container"""
    try:
        # Build the image
        dockerfile_path = Path(__file__).parent / 'Dockerfile'
        subprocess.run([
            'docker', 'build',
            '-t', 'dorker',
            '-f', str(dockerfile_path),
            '.'
        ], check=True)
        
        # Run the container
        subprocess.run([
            'docker', 'run', '-itd',
            '-p', '8080:8080',
            '-v', f'{DORKER_WORKSPACE}:/dorker_workspace',
            '--name=dorker',
            'dorker'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Failed to initialize dorker: {e}{Colors.WHITE}")
        return False
    return True

def show_help():
    """Display help information"""
    print(f"{Colors.BLUE}")
    print("Dorker is configured to run only inside", DORKER_WORKSPACE)
    print("Change settings in src/settings.py")
    print("Change Dockerfile in src/Dockerfile")
    print("\nAvailable commands:")
    # Add your commands here
    print(f"{Colors.WHITE}")

def main(args=None):
    """Main entry point for dorker command"""
    if not args or '-h' in args or '--help' in args:
        show_help()
        return
    
    if not check_environment():
        return
    
    # Add your command processing here 