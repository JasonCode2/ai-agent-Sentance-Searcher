from pydantic import BaseModel
from typing import Literal, Optional, Dict, Any

class AgentOutput(BaseModel):
    action: Literal["tool", "final"]
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    response: Optional[str] = None