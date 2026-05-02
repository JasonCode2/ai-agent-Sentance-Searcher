from tools.registry import TOOL_DESCRIPTIONS

def build_system_prompt():
    tool_list = "\n".join(
        [f"{name}: {desc}" for name, desc in TOOL_DESCRIPTIONS.items()]
    )

    return f"""
You are a tool-using AI agent.

Available tools:
{tool_list}

You must respond ONLY in valid JSON:

{{
  "action": "tool" or "final",
  "tool_name": "...",
  "tool_args": {{ }},
  "response": "..."
}}

Rules:
- When using "final", provide a clear, user-friendly answer
- Use tools when needed
- If answering directly, use "final"
- No extra text
"""