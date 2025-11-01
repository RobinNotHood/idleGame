# Building Milo's Cozy Adventures for Windows

This guide explains how to build a standalone Windows executable from the source code.

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Git** (to clone the repository)
   - Download from: https://git-scm.com/downloads

### Required Python Packages

All dependencies are listed in `requirements.txt`:
- pygame==2.5.2
- pyinstaller==6.3.0

## Step-by-Step Build Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/RobinNotHood/idleGame.git
cd idleGame
```

### 2. Set Up Python Environment (Recommended)

Using a virtual environment keeps dependencies isolated:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Pygame (game engine)
- PyInstaller (executable builder)

### 4. Test the Game (Optional but Recommended)

Before building, test that the game runs:

```bash
python main.py
```

You should see the game window open. Press the X to close.

### 5. Build the Executable

#### Option A: Using the Build Script (Easiest)

```bash
python build.py
```

This will automatically:
- Configure PyInstaller
- Build a single executable file
- Place it in the `dist/` folder

#### Option B: Using PyInstaller Directly

```bash
pyinstaller build.spec
```

Or, with custom options:

```bash
pyinstaller main.py \
  --name=MilosCozyAdventures \
  --onefile \
  --windowed \
  --clean
```

### 6. Locate Your Executable

After a successful build, find your executable at:

```
dist/MilosCozyAdventures.exe
```

### 7. Test the Executable

1. Navigate to the `dist/` folder
2. Double-click `MilosCozyAdventures.exe`
3. The game should launch without requiring Python

## Troubleshooting

### "Python is not recognized..."

- Python is not in your PATH
- Reinstall Python and check "Add Python to PATH"
- Or manually add Python to PATH

### "No module named 'pygame'"

- Virtual environment not activated, OR
- Dependencies not installed
- Run: `pip install -r requirements.txt`

### Build succeeds but .exe won't run

- **Antivirus blocking**: Some antivirus software flags PyInstaller executables
  - Add exception for the .exe or the dist/ folder
- **Missing dependencies**: Make sure all imports work when running `python main.py`

### "Permission denied" errors

- Close the game if it's running
- Close any file explorers viewing the dist/ folder
- Run the build script again

### Game runs from Python but not from .exe

- PyInstaller may have missed dependencies
- Check the `build/MilosCozyAdventures/warn-MilosCozyAdventures.txt` file for warnings
- Add any missing imports to `hiddenimports` in `build.spec`

## Distribution

The final executable (`MilosCozyAdventures.exe`) is completely standalone:

- ✅ Can be run on any Windows 10/11 computer
- ✅ No Python installation required
- ✅ No additional files needed
- ✅ Creates save file (`milo_save.json`) in the same directory when first run

### What to Distribute

**Minimum:**
- `MilosCozyAdventures.exe`

**Recommended:**
- `MilosCozyAdventures.exe`
- `README.md` (game instructions)

Users can simply:
1. Download the .exe
2. Double-click to play
3. Enjoy!

## Build Customization

### Changing the Executable Icon

1. Create or obtain a `.ico` file
2. Edit `build.spec` and change:
   ```python
   icon='NONE'
   ```
   to:
   ```python
   icon='path/to/icon.ico'
   ```

### Including Additional Files

To bundle assets, images, or data files:

Edit `build.spec` and add to the `datas` list:

```python
datas=[('assets', 'assets')],
```

### Changing Window Settings

To show a console window (useful for debugging):

In `build.spec`, change:
```python
console=False,
```
to:
```python
console=True,
```

## Build Performance

**Build Time:**
- First build: 2-5 minutes
- Subsequent builds: 1-3 minutes

**File Size:**
- Executable: ~15-25 MB (compressed)
- Uncompressed in memory: ~50-70 MB

**Optimizations:**

To reduce file size, edit `build.spec`:
```python
upx=True,  # Compress the executable
```

Note: UPX compression may trigger false positives in some antivirus software.

## Platform-Specific Notes

### Building on Windows for Windows
✅ Native and straightforward - use the instructions above

### Building on Linux for Windows
⚠️ Requires Wine and additional setup:
```bash
pip install pyinstaller
wine python -m PyInstaller build.spec
```

### Building on macOS for Windows
⚠️ Not recommended - use a Windows machine or VM

**Best Practice:** Always build on the target platform (Windows) for the most reliable results.

## Advanced: Creating an Installer

For professional distribution, you can create an installer using:

- **Inno Setup** (free): https://jrsoftware.org/isinfo.php
- **NSIS** (free): https://nsis.sourceforge.io/
- **Advanced Installer** (commercial)

This allows you to:
- Create desktop shortcuts
- Add to Start Menu
- Set up file associations
- Include uninstaller

## Continuous Integration

To automate builds on GitHub:

1. Create `.github/workflows/build.yml`
2. Use GitHub Actions to build on every commit
3. Automatically upload the .exe as a release artifact

Example workflow file available on request.

## Questions?

If you encounter issues not covered here:
1. Check PyInstaller documentation: https://pyinstaller.org/
2. Check Pygame documentation: https://www.pygame.org/docs/
3. Open an issue on the GitHub repository

---

Happy building! 🛠️
