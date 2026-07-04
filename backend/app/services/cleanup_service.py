import threading
import time
from pathlib import Path


def delete_later(file_path: Path, delay: int = 900):
    """
    delay dalam detik
    default = 300 detik (5 menit)
    """

    def worker():
        time.sleep(delay)

        if file_path.exists():
            try:
                file_path.unlink()
                print(f"[AUTO DELETE] {file_path.name}")
            except Exception as e:
                print(e)

    threading.Thread(target=worker, daemon=True).start()