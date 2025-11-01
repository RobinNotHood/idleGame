"""
Build script for creating Windows executable
Run this to create MilosCozyAdventures.exe
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable using PyInstaller"""

    # PyInstaller options
    options = [
        'main.py',                          # Main script
        '--name=MilosCozyAdventures',       # Name of the exe
        '--onefile',                        # Single executable file
        '--windowed',                       # No console window
        '--icon=NONE',                      # No icon (could add custom later)
        '--clean',                          # Clean cache
        '--noconfirm',                      # Overwrite without asking
        # Add any data files if needed
        # '--add-data=assets:assets',
    ]

    print("Building Milo's Cozy Adventures executable...")
    print("This may take a few minutes...")

    try:
        PyInstaller.__main__.run(options)
        print("\n" + "="*60)
        print("BUILD SUCCESSFUL!")
        print("="*60)
        print(f"\nExecutable created: dist/MilosCozyAdventures.exe")
        print("\nYou can now distribute this .exe file!")
        print("The game will create a save file (milo_save.json) in the same directory.")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
