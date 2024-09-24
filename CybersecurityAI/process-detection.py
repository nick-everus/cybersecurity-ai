import psutil

# List of known good processes (whitelist)
whitelisted_processes = ["sshd", "bash", "nginx", "python3"]

def detect_suspicious_processes():
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            # If the process is not in the whitelist
            if proc.info['name'] not in whitelisted_processes:
                print(f"Suspicious process detected: {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

if __name__ == "__main__":
    detect_suspicious_processes()