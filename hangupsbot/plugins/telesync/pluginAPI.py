commands = []

def tg_command_register(bot, cmd, shared_func):
    global commands
    commands[cmd] = shared_func
    bot.call_shared("telesync.add_command", cmd, tg_command_wrapper)

def tg_command_wrapper(bot, chat_id, args, cmd):
    params = args['params']

    tg2ho_dict = bot.ho_bot.memory.get_by_path(['telesync'])['tg2ho']
    if str(chat_id) in tg2ho_dict:
        ho_conv_id = tg2ho_dict[str(chat_id)]
        tldr_args = {'params': params, 'conv_id': ho_conv_id}
        global commands
        try:
            text = bot.ho_bot.call_shared(commands[cmd], bot.ho_bot, tldr_args)
            yield from bot.sendMessage(chat_id, text, parse_mode='HTML')
        except KeyError as ke:
            yield from bot.sendMessage(chat_id, "{cmd} plugin is not active. KeyError: {e}".format(e=ke, cmd=cmd))
            
