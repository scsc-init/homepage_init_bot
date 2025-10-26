from src.bot.discord import SCSCBotConnector


async def create_sig(connector: SCSCBotConnector, body: dict):
    connector.create_sig(
        body["sig_name"], body["user_id_list"], body.get("sig_description", None)
    )


async def archive_sig(connector: SCSCBotConnector, body: dict):
    connector.archive_sig(body["sig_name"], previous_semester=body["previous_semester"])


async def create_pig(connector: SCSCBotConnector, body: dict):
    connector.create_pig(
        body["pig_name"], body["user_id_list"], body.get("pig_description", None)
    )


async def archive_pig(connector: SCSCBotConnector, body: dict):
    connector.archive_pig(body["pig_name"], previous_semester=body["previous_semester"])


async def edit_sig(connector: SCSCBotConnector, body: dict):
    connector.edit_sig(
        body["sig_name"], body.get("new_sig_name", None), body.get("new_topic", None)
    )


async def edit_pig(connector: SCSCBotConnector, body: dict):
    connector.edit_pig(
        body["pig_name"], body.get("new_pig_name", None), body.get("new_topic", None)
    )
