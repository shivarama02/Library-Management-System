#!/usr/bin/env python3
"""
Setup script for BookHub project
This script helps set up the development environment
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def setup_backend():
    """Set up the Django backend"""
    print("Setting up Django backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("Backend directory not found!")
        return False
    
    # Check if virtual environment exists
    env_dir = backend_dir / "env"
    if not env_dir.exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv env", cwd=backend_dir):
            return False
    
    # Activate virtual environment and install requirements
    print("Installing Python dependencies...")
    if os.name == 'nt':  # Windows
        pip_cmd = "env\\Scripts\\pip install -r requirements.txt"
    else:  # Unix/Linux/macOS
        pip_cmd = "env/bin/pip install -r requirements.txt"
    
    if not run_command(pip_cmd, cwd=backend_dir):
        return False
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    env_file_template = backend_dir / "env_file.txt"
    
    if not env_file.exists() and env_file_template.exists():
        print("Creating .env file from template...")
        os.rename(env_file_template, env_file)
    
    print("Backend setup completed!")
    return True

def setup_frontend():
    """Set up the React frontend"""
    print("Setting up React frontend...")
    
    frontend_dir = Path("frontend/bookapp")
    if not frontend_dir.exists():
        print("Frontend directory not found!")
        return False
    
    # Install npm dependencies
    print("Installing Node.js dependencies...")
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    print("Frontend setup completed!")
    return True

def main():
    """Main setup function"""
    print("BookHub Setup Script")
    print("====================")
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("Error: Please run this script from the project root directory!")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("Frontend setup failed!")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("Setup completed successfully!")
    print("="*50)
    print("\nNext steps:")
    print("1. Navigate to backend directory: cd backend")
    print("2. Activate virtual environment:")
    print("   - Windows: env\\Scripts\\activate")
    print("   - Unix/Linux/macOS: source env/bin/activate")
    print("3. Update .env file with your database credentials")
    print("4. Run migrations: python manage.py makemigrations && python manage.py migrate")
    print("5. Start backend: python manage.py runserver")
    print("6. In another terminal, navigate to frontend/bookapp")
    print("7. Start frontend: npm start")
    print("\nHappy coding! 🚀")

if __name__ == "__main__":
    main() 