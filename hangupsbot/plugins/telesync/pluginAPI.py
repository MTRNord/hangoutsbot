commands = {}

class Event(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, conv_id, conv):
        self.conv_id = conv_id
        self.conv = conv
        
class Bot(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, coro_send_message):
        self.coro_send_message = coro_send_message

def tg_command_register(bot, cmd, shared_func):
    global commands
    commands[cmd] = shared_func
    bot.call_shared("telesync.add_command", cmd, tg_command_wrapper)

def tg_command_wrapper(bot, chat_id, args, cmd):
    params = args['params'][0]
    event = Event(chat_id, chat_id)
    ho_bot = Bot(bot.sendMessage(chat_id, msg))
    tg2ho_dict = bot.ho_bot.memory.get_by_path(['telesync'])['tg2ho']
    if str(chat_id) in tg2ho_dict:
        ho_conv_id = tg2ho_dict[str(chat_id)]
        global commands
        
        try:
            yield from commands[cmd](bot.ho_bot, event, params)
            yield from bot.sendMessage(chat_id, text, parse_mode='HTML')
        except KeyError as ke:
            yield from bot.sendMessage(chat_id, "{cmd} plugin is not active. KeyError: {e}".format(e=ke, cmd=cmd))
            
