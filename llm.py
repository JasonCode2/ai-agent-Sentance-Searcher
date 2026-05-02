import requests
import subprocess
import os
from config import MODEL_NAME, AUTO_PULL
from log_util import log_llm_request, log_llm_response

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_PATH = os.path.join("ollama", "ollama.exe")


def ensure_model():
    if not AUTO_PULL:
        return

    print(f"Checking model: {MODEL_NAME}")

    # check installed models
    try:
        res = requests.get("http://localhost:11434/api/tags")
        models = [m["name"] for m in res.json().get("models", [])]

        if MODEL_NAME not in models:
            print(f"Model not found. Pulling {MODEL_NAME}...")
            subprocess.run([OLLAMA_PATH, "pull", MODEL_NAME])
        else:
            print("Model already installed.")

    except Exception as e:
        print("Could not verify model:", e)


def call_llm(messages):
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

    req_json = {"model": MODEL_NAME, "prompt": prompt, "stream": False}

    try:
        # Log request
        try:
            log_llm_request(req_json)
        except Exception:
            pass

        response = requests.post(OLLAMA_URL, json=req_json)
        resp_json = response.json()

        # Log response
        try:
            log_llm_response(resp_json, raw_text=resp_json.get("response"))
        except Exception:
            pass

        return resp_json["response"]
    except Exception as e:
        try:
            log_llm_response({"error": str(e)})
        except Exception:
            pass
        raise