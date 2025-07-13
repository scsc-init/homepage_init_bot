from src.controller import create_invite, send_message_by_id, send_message_by_name, get_id_from_name
from src.controller import give_role_to_id, remove_role_from_id, get_ids_from_name, create_role_with_ids
from src.controller import update_sig_category, update_sig_archive_category, get_category_from_name, create_channel, move_channel, update_data, update_pig_archive_category, update_pig_category
from src.controller import create_sig, archive_sig, create_pig, archive_pig

_ACTION_MAP = {
    1001: create_invite,
    1002: send_message_by_id,
    1003: send_message_by_name,
    1004: get_id_from_name,
    2001: give_role_to_id,
    2002: remove_role_from_id,
    2003: get_ids_from_name,
    2004: create_role_with_ids,
    3001: update_sig_category,
    3002: update_sig_archive_category,
    3003: update_pig_category,
    3004: update_pig_archive_category,
    3005: get_category_from_name,
    3006: create_channel,
    3007: move_channel,
    3008: update_data,
    4001: create_sig,
    4002: archive_sig,
    4003: create_pig,
    4004: archive_pig,
}

def dispatch(action_code: int):
    handler = _ACTION_MAP.get(action_code)
    if not handler:
        raise ValueError(f"Unknown action code: {action_code}")
    return handler
