# AetherFold 🌌📂

Autonomous, agentic file manager powered by LangGraph and Gemini 1.5 Pro.

AetherFold is a smart, stateful file organization agent that keeps your Desktop clean by categorizing files into a logical directory structure.

## Core Concepts

- **AetherFold Storage:** This is the root directory where your files are moved. By default, it's inside this project under `storage/`.
- **Intelligent Trash:** Gemini 1.5 Pro identifies screenshots, temporary installers, and junk files, suggesting they be moved to a `Trash/` folder for your review.
- **Human-in-the-Loop:** No file is ever moved without your explicit approval via the CLI.

## Setup

1. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Copy `.env.example` to `.env` and add your Google API Key.
   ```bash
   cp .env.example .env
   ```

4. **Run AetherFold:**
   ```bash
   python3 main.py
   ```

## macOS Startup Instructions

To have AetherFold scan your Desktop every time you log in:
1. Run `./scripts/setup_startup.sh`.
2. Add the generated `launch_aetherfold.sh` as a login item in 'System Settings' -> 'General' -> 'Login Items'.

## Features
- **Intelligent Peeking:** Extracts text from the first page of PDFs and the first 500 chars of text files to categorize by actual content.
- **Categorization & Deletion:** Automatically identifies categories (Work, Finance, Media, etc.) and flags redundant files for deletion.
- **Safety Breakpoint:** Provides a clear Move Plan with `[MOVE]` and `[TRASH/DELETE]` labels before execution.
- **Stateful Memory:** Uses LangGraph's checkpointer to maintain session context.
