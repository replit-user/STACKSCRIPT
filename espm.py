import requests
import argparse
import os
import zipfile
import shutil
import re  # For input sanitization
import asyncio
BASE_URL = "espm-backend.onrender.com"

parser = argparse.ArgumentParser(description="the official STACKSCRIPT package manager")
parser.add_argument("command", help="command to run", choices=["install", "uninstall", "publish", "update"])
parser.add_argument("name", help="name of the module")
parser.add_argument("--version", "-v", help="version identifier",default="latest")
args = parser.parse_args()

def validate_name(name):
    """Basic sanitization for module names"""
    if not re.match(r'^[\w-]+$', name):
        print(f"Invalid module name: {name}")
        exit(1)

def safe_delete(path):
    """Secure file/directory removal"""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)
async def main():
    if args.command == "install":
        if not args.version:
            print("Version is required for install")
            exit(1)
        
        validate_name(args.name)
        response = requests.get(f"https://{BASE_URL}/download/{args.name}/{args.version}")
        
        if response.status_code == 200:
            zip_filename = f"{args.name}.zip"
            with open(zip_filename, "wb") as f:
                f.write(response.content)
            
            # Extract and clean up
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(".")
            os.remove(zip_filename)
            print(f"Installed {args.name}@{args.version}")
            
    elif args.command == "uninstall":
        validate_name(args.name)
        safe_delete(f"{args.name}.stack")
        safe_delete(f"{args.name}.stackm")
        print(f"Uninstalled {args.name}")

    elif args.command == "publish":
        if not args.version:
            print("Version identifier required")
            exit(1)
        
        validate_name(args.name)
        stack_file = f"{args.name}.stack"
        stackm_file = f"{args.name}.stackm"
        
        if not all(map(os.path.exists, [stack_file, stackm_file])):
            print("Missing .stack or .stackm file")
            exit(1)
        
        with open(stack_file, "rb") as s, open(stackm_file, "rb") as m:
            response = requests.post(
                url=f"https://{BASE_URL}/upload",
                data={"name": args.name, "version": args.version},
                files={"stack": s, "stackm": m}
            )
        
        print("Publication successful" if response.ok else f"Error: {response.text}")

    elif args.command == "update":
        if not args.version:
            print("Version identifier required")
            exit(1)
        
        validate_name(args.name)
        stack_file = f"{args.name}.stack"
        stackm_file = f"{args.name}.stackm"
        
        if not all(map(os.path.exists, [stack_file, stackm_file])):
            print("Missing .stack or .stackm file")
            exit(1)
        
        with open(stack_file, "rb") as s, open(stackm_file, "rb") as m:
            response = requests.post(
                url=f"https://{BASE_URL}/update/{args.name}/{args.version}",
                files={"stack": s, "stackm": m}
            )
        
        print("Update successful" if response.ok else f"Error: {response.text}")

asyncio.run(main())