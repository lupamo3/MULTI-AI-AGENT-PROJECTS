import subprocess
import threading
import time
from pathlib import Path
import os

from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_backend():
    try:
        logger.info("starting backend service..")
        env = os.environ.copy()
        # make sure backend also has root on PYTHONPATH
        env["PYTHONPATH"] = f"{PROJECT_ROOT}:{env.get('PYTHONPATH', '')}"
        subprocess.run(
            [
                "uvicorn",
                "app.backend.api:app",
                "--host",
                "127.0.0.1",
                "--port",
                "9999",
            ],
            check=True,
            env=env,
            cwd=PROJECT_ROOT,
        )
    except CustomException as e:
        logger.error("Problem with backend service")
        raise CustomException("Failed to start backend", e)


def run_frontend():
    try:
        logger.info("Starting Frontend service")
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{PROJECT_ROOT}:{env.get('PYTHONPATH', '')}"

        subprocess.run(
            ["streamlit", "run", "app/frontend/ui.py"],
            check=True,
            env=env,
            cwd=PROJECT_ROOT,
        )
    except CustomException as e:
        logger.error("Problem with frontend service")
        raise CustomException("Failed to start frontend", e)


if __name__ == "__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()
    except CustomException as e:
        logger.exception(f"CustomException occured : {str(e)}")
