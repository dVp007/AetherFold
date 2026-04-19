import os
import shutil
from typing import List, Optional
from pypdf import PdfReader
from .schema import FileInfo, MovePlan

def scan_desktop(desktop_path: str) -> List[FileInfo]:
    files = []
    for item in os.listdir(desktop_path):
        full_path = os.path.join(desktop_path, item)
        if os.path.isfile(full_path) and not item.startswith('.'):
            files.append(FileInfo(name=item, path=full_path))
    return files

def peek_file(file_path: str, char_limit: int = 500) -> str:
    _, ext = os.path.splitext(file_path.lower())
    try:
        if ext == '.pdf':
            reader = PdfReader(file_path)
            first_page = reader.pages[0]
            return first_page.extract_text()[:char_limit]
        elif ext in ['.txt', '.md', '.py', '.json', '.csv', '.log']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(char_limit)
    except Exception as e:
        return f"Error reading file: {str(e)}"
    return f"Peek not available for extension: {ext}"

def execute_move(plan: List[MovePlan]):
    for move in plan:
        dest_dir = os.path.dirname(move.destination)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        try:
            shutil.move(move.source, move.destination)
            print(f"Moved: {move.source} -> {move.destination}")
        except Exception as e:
            print(f"Failed to move {move.source}: {e}")
