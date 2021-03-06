"""
Plugin for monitoring if bot is added to a HO and report it to the bot admins.
Add a "botaddnotif_enable": true  parameter in the config.json file.

Author: @cd334
"""

import asyncio
import hangups
import plugins

def _initialise(bot):
    plugins.register_handler(_handle_join_notify, type="membership")

@asyncio.coroutine
def _handle_join_notify(bot, event, command):
    if not event.conv_event.type_ == hangups.MembershipChangeType.JOIN:
        return

    # has bot been added to a new hangout?
    bot_id = bot._user_list._self_user.id_
    if not bot_id in event.conv_event.participant_ids:
        return

    if not bot.get_config_option("botaddnotif_enable"):
        return

    # send message to admins
    message = u'<b>%s</b> has added me to Hangout: <b>%s</b>' % (event.user.full_name, event.conv.name)
    for admin_id in bot.get_config_option('admins'):
        yield from bot.coro_send_to_user(admin_id, message)
