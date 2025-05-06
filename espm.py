import requests
import argparse
import os
import zipfile
import shutil
import re

BASE_URL = "espm-backend.onrender.com"

parser = argparse.ArgumentParser(description="The official STACKSCRIPT package manager")
parser.add_argument("command", help="Command to run", choices=["install", "uninstall", "publish", "update", "list"])
parser.add_argument("--name", "-n", help="Name of the module", required=False)
parser.add_argument("--version", "-v", help="Version identifier", default="latest")

def validate_name(name):
    if not re.match(r'^[\w-]+$', name):
        print(f"Invalid module name: {name}")
        exit(1)

def safe_delete(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def main():
    args = parser.parse_args()

    if args.command == "install":
        if not args.name or not args.version:
            print("Module name and version are required for install")
            exit(1)
        validate_name(args.name)
        response = requests.get(f"https://{BASE_URL}/download/{args.name}/{args.version}")
        if response.status_code != 200:
            print(f"Failed to install {args.name}@{args.version}: {response.text}")
            exit(1)
        zip_filename = f"{args.name}.zip"
        with open(zip_filename, "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(".")
        os.remove(zip_filename)
        print(f"Installed {args.name}@{args.version}")

    elif args.command == "uninstall":
        if not args.name:
            print("Module name is required for uninstall")
            exit(1)
        validate_name(args.name)
        safe_delete(f"{args.name}.stack")
        safe_delete(f"{args.name}.stackm")
        print(f"Uninstalled {args.name}")

    elif args.command == "publish":
        if not args.name or not args.version:
            print("Module name and version are required for publish")
            exit(1)
        validate_name(args.name)
        stack_file = f"{args.name}.stack"
        stackm_file = f"{args.name}.stackm"
        if not os.path.exists(stack_file) or not os.path.exists(stackm_file):
            print("Missing .stack or .stackm file")
            exit(1)
        with open(stack_file, "rb") as s, open(stackm_file, "rb") as m:
            response = requests.post(
                f"https://{BASE_URL}/upload",
                files={"stack": s, "stackm": m},
                data={"name": args.name, "version": args.version}
            )
        if response.status_code == 200:
            print("Publication successful")
        else:
            print(f"Publication failed: {response.text}")

    elif args.command == "update":
        if not args.name or not args.version:
            print("Module name and version are required for update")
            exit(1)
        validate_name(args.name)
        stack_file = f"{args.name}.stack"
        stackm_file = f"{args.name}.stackm"
        if not os.path.exists(stack_file) or not os.path.exists(stackm_file):
            print("Missing .stack or .stackm file")
            exit(1)
        with open(stack_file, "rb") as s, open(stackm_file, "rb") as m:
            response = requests.post(
                f"https://{BASE_URL}/update/{args.name}/{args.version}",
                files={"stack": s, "stackm": m}
            )
        if response.status_code == 200:
            print("Update successful")
        else:
            print(f"Update failed: {response.text}")

    elif args.command == "list":
        response = requests.get(f"https://{BASE_URL}/modules")
        if response.status_code == 200:
            modules = response.json()
            for name, versions in modules.items():
                print(f"{name} (versions: {', '.join(versions)})")
        else:
            print(f"Error fetching modules: {response.text}")

if __name__ == "__main__":
    main()