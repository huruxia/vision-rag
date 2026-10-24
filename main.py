import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from vision_rag.chat_cli import run

run()
