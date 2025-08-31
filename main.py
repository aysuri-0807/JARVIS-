from Dependencies import *
from SETUP import *

words = []


while True:
    message = listen()
    message = message.lower()
    print (message)
    for word in message.split():
        words.append(word)
    for word in words:
        try:
            if "open" in words:
                idx = apps.index(word)
                open_app(apps[idx])
                print (f"Opening {apps[idx]}")
                readAloud(f"Opening {apps[idx]}")
                words.clear()
            else:
                print ("NO COMMAND GIVEN. TRY AGAIN")
                words.clear()
        except:
            pass


