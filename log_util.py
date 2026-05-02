import os
import json
import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_PATH = os.path.join(BASE_DIR, "log.txt")


# ---------------------------
# Utilities
# ---------------------------

def _timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"


def clear_log():
    try:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        pass


def _safe_json(obj):
    """
    Convert anything into a clean JSON-serializable structure.
    """
    try:
        return json.loads(json.dumps(obj, default=str, ensure_ascii=False))
    except Exception:
        return str(obj)


def _append(entry_type, payload):
    entry = {
        "timestamp": _timestamp(),
        "type": entry_type,
        "payload": _safe_json(payload)
    }

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write("\n")
    except Exception:
        pass


# ---------------------------
# LLM Logging
# ---------------------------

def log_llm_request(request_json):
    """
    Logs ONLY what the model was asked.
    """
    cleaned = {
        "model": request_json.get("model"),
        "prompt": request_json.get("prompt"),
    }
    _append("llm_request", cleaned)


def log_llm_response(response_json, raw_text=None):
    """
    Logs ONLY the model's actual decision output.
    Strips all backend noise (context, eval stats, etc.)
    """
    cleaned = {}

    if isinstance(response_json, dict):
        cleaned = {
            "model": response_json.get("model"),
            "response": response_json.get("response"),
            "done_reason": response_json.get("done_reason"),
        }

    payload = {"response": cleaned}

    if raw_text:
        payload["raw_text"] = raw_text

    _append("llm_response", payload)


def log_model_output(raw_text, parsed_json=None):
    """
    Logs raw model text + parsed structured output.
    """
    _append("model_output", {
        "raw_text": raw_text,
        "parsed": _safe_json(parsed_json)
    })


# ---------------------------
# Tool Logging
# ---------------------------

def log_tool_call(tool_name, args, result):
    """
    Logs tool execution in human-readable form.
    """
    _append("tool_call", {
        "tool": tool_name,
        "args": _safe_json(args),
        "result": _safe_json(result)
    })


# ---------------------------
# Optional: High-level event log
# ---------------------------

def log_event(message):
    """
    Optional helper for debugging flow.
    """
    _append("event", {"message": message})