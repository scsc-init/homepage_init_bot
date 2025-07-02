from src.controller import create_invite, send_message_by_id, send_message_by_name, get_id_from_name
from src.controller import give_role_to_id, remove_role_from_id, get_ids_from_name, create_role_with_ids

_ACTION_MAP = {
    1001: create_invite,
    1002: send_message_by_id,
    1003: send_message_by_name,
    1004: get_id_from_name,
    2001: give_role_to_id,
    2002: remove_role_from_id,
    2003: get_ids_from_name,
    2004: create_role_with_ids,
}

def dispatch(action_code: int):
    handler = _ACTION_MAP.get(action_code)
    if not handler:
        raise ValueError(f"Unknown action code: {action_code}")
    return handler
