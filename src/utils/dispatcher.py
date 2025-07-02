from src.controller import create_invite

_ACTION_MAP = {
    1001: create_invite
}

def dispatch(action_code: int):
    handler = _ACTION_MAP.get(action_code)
    if not handler:
        raise ValueError(f"Unknown action code: {action_code}")
    return handler
