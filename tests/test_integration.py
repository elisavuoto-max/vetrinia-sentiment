import json
import os
import pickle
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.fake_model import FakeSentimentModel


def wait_for_server(process, timeout=15):
    """Attende che Flask inizi ad ascoltare sulla porta 5000."""
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                f"Il processo Flask è terminato con codice {process.returncode}"
            )

        try:
            with socket.create_connection(
                ("127.0.0.1", 5000), timeout=0.5
            ):
                return
        except OSError:
            time.sleep(0.2)

    raise TimeoutError("Flask non si è avviato entro il tempo previsto")


def test_application_with_serialized_model(tmp_path):
    model_path = tmp_path / "sentiment_analysis_model.pkl"

    with open(model_path, "wb") as file:
        pickle.dump(FakeSentimentModel(), file)

    env = os.environ.copy()
    env["MODEL_PATH"] = str(model_path)
    env["PYTHONPATH"] = (
        str(ROOT)
        + os.pathsep
        + env.get("PYTHONPATH", "")
    )

    process = subprocess.Popen(
        [sys.executable, str(ROOT / "app" / "app.py")],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        wait_for_server(process)

        request = urllib.request.Request(
            "http://127.0.0.1:5000/predict",
            data=json.dumps(
                {"review": "I love this product"}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                body = json.loads(response.read().decode("utf-8"))

                assert response.status == 200
                assert body["sentiment"] == "positive"

        except urllib.error.HTTPError as exc:
            output = process.stdout.read() if process.poll() is not None else ""
            raise AssertionError(
                f"HTTP {exc.code}: {exc.read().decode('utf-8')}\n"
                f"Log Flask:\n{output}"
            ) from exc

    finally:
        if process.poll() is None:
            process.terminate()

        try:
            output, _ = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            output, _ = process.communicate()

        if process.returncode not in (0, -15, 1, 130):
            print(f"Output del processo Flask:\n{output}")