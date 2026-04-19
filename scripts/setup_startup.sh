#!/bin/bash

# Setup AetherFold as a macOS Login Item

PROJECT_DIR=$(pwd)
VENV_PATH="$PROJECT_DIR/venv"
MAIN_SCRIPT="$PROJECT_DIR/main.py"

if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Please run 'python3 -m venv venv' first."
    exit 1
fi

# Create a launcher script
LAUNCHER="$PROJECT_DIR/launch_aetherfold.sh"
echo "#!/bin/bash
cd \"$PROJECT_DIR\"
source \"$VENV_PATH/bin/activate\"
python3 \"$MAIN_SCRIPT\"" > "$LAUNCHER"
chmod +x "$LAUNCHER"

echo "Launcher script created at: $LAUNCHER"
echo ""
echo "To set this as a login item on macOS:"
echo "1. Open 'System Settings' -> 'General' -> 'Login Items'."
echo "2. Click '+' and select the '$LAUNCHER' file."
echo "3. Alternatively, use 'Automator' to create an App that runs this shell script."
