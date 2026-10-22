import subprocess, sys, os

FILE_NAME = "trash (galaxy a10)"+".txt"
KEEP_DATA = False 

def debloat(file_path):
    if not os.path.exists(file_path):
        print(f"{file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    success_count = 0
    already_removed_count = 0
    error_count = 0

    for pkg in packages:
        print(f"Process {pkg}...", end=" ", flush=True)
        
        try:
            cmd = ["adb", "shell", "pm", "uninstall"]
            if KEEP_DATA:
                cmd.append("-k")
            cmd.extend(["--user", "0", pkg])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            output = result.stdout.strip()
            
            if "Success" in output:
                print(f"deleted: {pkg}")
                success_count += 1
            elif "Failure [not installed for 0]" in output:
                print(f"not found: {pkg}")
                already_removed_count += 1
            else:
                print(f"cannot delete: {pkg}")
                print(output)
                error_count += 1
                
        except Exception as e:
            print(e)
            error_count += 1

    print(f"Total: {len(packages)}")
    print(f"Deleted: {success_count}")
    print(f"Cannot delete: {error_count}")
    print(f"Not found: {already_removed_count}")
    
if __name__ == "__main__":
    check = subprocess.run(["adb", "get-state"], capture_output=True, text=True)
    if "device" not in check.stdout:
        print("Device is not connected")
        sys.exit(1)
        
    debloat(FILE_NAME)