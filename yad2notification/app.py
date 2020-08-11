import eel
from Yad2Bot import *
from threading import *


@eel.expose
def start_search(url, phone):
    global new_bot
    new_bot = Yad2Bot(url, phone)
    t = Thread(target=new_bot.start_search)
    t.start()


@eel.expose
def stop_search():
    global new_bot
    new_bot.stop()
    return True


@eel.expose
def get_all():
    global new_bot
    posts_list = new_bot.get_all()
    return posts_list


eel.init('web')
try:
    eel.start('index.html', size=(850, 440), port=2323)
except (SystemExit, MemoryError, KeyboardInterrupt):
    print("Program Exit, Save Logs if Needed")
