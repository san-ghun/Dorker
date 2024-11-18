import os
import time
import subprocess
from .settings import Colors

def check_docker_running():
    try:
        subprocess.run(['docker', 'stats', '--no-stream'], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def open_docker():
    if not check_docker_running():
        print(f"{Colors.GREEN}Docker is starting up...{Colors.WHITE}", end='', flush=True)
        subprocess.run(['open', '-g', '-a', 'Docker'])
        
        while not check_docker_running():
            print(f"{Colors.GREEN}.{Colors.WHITE}", end='', flush=True)
            time.sleep(1)
        print()
    else:
        print(f"{Colors.BLUE}Docker is already running{Colors.WHITE}")

def setup_goinfre_docker():
    user = os.environ.get('USER')
    docker_dest = f"/goinfre/{user}/docker"
    
    # Check if docker already exists in goinfre
    if os.path.exists(docker_dest):
        response = input(f"{Colors.RED}Docker is already setup in {docker_dest}, do you want to reset it? [y/N]{Colors.WHITE}")
        if response.lower() == 'y':
            subprocess.run(['rm', '-rf', f"{docker_dest}/com.docker.docker",
                          f"{docker_dest}/com.docker.helper",
                          f"{docker_dest}/.docker"])

    # Remove existing symlinks and directories
    paths_to_clean = [
        '~/Library/Containers/com.docker.docker',
        '~/Library/Containers/com.docker.helper',
        '~/.docker'
    ]
    
    for path in paths_to_clean:
        expanded_path = os.path.expanduser(path)
        try:
            if os.path.islink(expanded_path):
                os.unlink(expanded_path)
            elif os.path.exists(expanded_path):
                subprocess.run(['rm', '-rf', expanded_path])
        except Exception:
            pass

    # Create destination directories
    os.makedirs(f"{docker_dest}/com.docker.docker", exist_ok=True)
    os.makedirs(f"{docker_dest}/com.docker.helper", exist_ok=True)
    os.makedirs(f"{docker_dest}/.docker", exist_ok=True)

    # Create symlinks
    links = [
        (f"{docker_dest}/com.docker.docker", "~/Library/Containers/com.docker.docker"),
        (f"{docker_dest}/com.docker.helper", "~/Library/Containers/com.docker.helper"),
        (f"{docker_dest}/.docker", "~/.docker")
    ]
    
    for src, dst in links:
        dst = os.path.expanduser(dst)
        os.symlink(src, dst)

    print(f"{Colors.GREEN}docker is now set up in goinfre{Colors.WHITE}") 