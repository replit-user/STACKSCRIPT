# frontend.py (CLI Frontend)
import argparse
import requests
import os

BASE_URL = "https://espm-backend.onrender.com"  # Update with your deployed URL

def install_package(package_name, version=None):
    try:
        url = f"{BASE_URL}/packages/{package_name}"
        params = {"version": version} if version else None
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        with open(f"{package_name}.stack", "w") as f:
            f.write(data["stack"])
        with open(f"{package_name}.stackm", "w") as f:
            f.write(data["stackm"])
        print(f"Installed {package_name} successfully!")
        
    except requests.exceptions.RequestException as e:
        print(f"Error installing package: {str(e)}")

def uninstall_package(package_name):
    try:
        os.remove(f"{package_name}.stack")
        os.remove(f"{package_name}.stackm")
        print(f"Uninstalled {package_name} successfully!")
    except FileNotFoundError:
        print(f"Package {package_name} not installed!")

def list_installed():
    files = [f for f in os.listdir('.') if f.endswith('.stack')]
    packages = [f[:-6] for f in files if f.endswith('.stack')]
    print("Installed packages:")
    for pkg in packages:
        print(f"- {pkg}")

def upload_package(package_name, version):
    stack_file = f"{package_name}.stack"
    stackm_file = f"{package_name}.stackm"
    
    if not (os.path.exists(stack_file)) and os.path.exists(stackm_file):
        print("Both .stack and .stackm files must exist!")
        return
        
    try:
        with open(stack_file, "r") as f:
            stack_content = f.read()
        with open(stackm_file, "r") as f:
            stackm_content = f.read()
            
        response = requests.post(
            f"{BASE_URL}/packages/{package_name}/upload",
            json={
                "version": version,
                "stack": stack_content,
                "stackm": stackm_content
            }
        )
        response.raise_for_status()
        print(f"Uploaded {package_name} version {version} successfully!")
        
    except Exception as e:
        print(f"Upload failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="ESPM Package Manager")
    subparsers = parser.add_subparsers(dest="command")

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("package_name")
    install_parser.add_argument("-v", "--version", dest="version")
    install_parser.add_argument("-u", "--upgrade", action="store_true")

    subparsers.add_parser("list")

    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.add_argument("package_name")

    upload_parser = subparsers.add_parser("upload")
    upload_parser.add_argument("package_name")
    upload_parser.add_argument("-u", "--upgrade", dest="version")
    upload_parser.add_argument("-v", "--version", dest="version")

    args = parser.parse_args()

    if args.command == "install":
        install_package(args.package_name, args.version)
    elif args.command == "list":
        list_installed()
    elif args.command == "uninstall":
        uninstall_package(args.package_name)
    elif args.command == "upload":
        if not args.version:
            print("Version is required for upload!")
            return
        upload_package(args.package_name, args.version)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()