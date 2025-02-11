import os
from typing import Optional
from loguru import logger

def get_env_variable(variable_name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(variable_name)
    if value is None:
        raise ValueError(f"Variable '{variable_name}' not found in environment.")
    return value