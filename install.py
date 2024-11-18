import os
from pathlib import Path

def install_dorker():
    """Install dorker by adding it to the user's shell configuration"""
    # Get the absolute path of the dorker init script
    init_script = Path(__file__).parent / 'init.py'
    init_script = init_script.resolve()
    
    # Determine which shell config file to use
    shell = os.environ.get('SHELL', '').split('/')[-1]
    config_file = Path.home() / f'.{shell}rc'
    
    if not config_file.exists():
        print(f"Could not find shell config file: {config_file}")
        return
    
    # Check if dorker is already installed
    with open(config_file, 'r') as f:
        if str(init_script) in f.read():
            print("Dorker already installed")
            return
    
    # Add dorker initialization to shell config
    with open(config_file, 'a') as f:
        f.write(f"\n# Dorker commands\n")
        f.write(f"python3 {init_script}\n")
    
    print("Dorker successfully installed")

if __name__ == "__main__":
    install_dorker() 