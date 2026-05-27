#!/bin/bash

echo "===================================="
echo "Lightcurve setup starting..."
echo "===================================="

# 1. Check for Homebrew
if ! command -v brew &> /dev/null
then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2. Ensure command line tools exist
if ! xcode-select -p &> /dev/null
then
    echo "Installing Apple Command Line Tools..."
    xcode-select --install
    echo "Please complete the popup install, then re-run script"
    exit 1
fi

# 3. Install Python + Git
brew install python git

# 4. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 5. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "===================================="
echo "Setup complete!"
echo "Run your app with:"
echo "  make run"
echo "===================================="
