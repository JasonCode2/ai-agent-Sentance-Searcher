import json
from schema import AgentOutput
from llm import call_llm
from tools.registry import TOOLS
from prompts.system_prompt import build_system_prompt
from log_util import log_model_output, log_tool_call

def safe_parse(text):
    try:
        return AgentOutput(**json.loads(text))
    except:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1:
            try:
                return AgentOutput(**json.loads(text[start:end]))
            except:
                pass
    return None

def run_agent(user_input):
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_input}
    ]

    for _ in range(5):
        response = call_llm(messages)
        # Log raw model output
        try:
            parsed = safe_parse(response)

            log_model_output(
                raw_text=response,
                parsed_json=parsed.dict() if parsed else None
            )
        except Exception:
            pass
        print("MODEL:", response)

        parsed = safe_parse(response)
        if not parsed:
            return "Error: bad model output"

        if parsed.action == "tool":
            tool = TOOLS.get(parsed.tool_name)

            if not tool:
                return f"Unknown tool: {parsed.tool_name}"

            result = tool(**parsed.tool_args)

            # Log tool usage and result
            try:
                log_tool_call(parsed.tool_name, parsed.tool_args or {}, result)
            except Exception:
                pass

            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "tool", "content": str(result)})

        elif parsed.action == "final":
            return parsed.response

    return "Max steps reached"