import requests
import os
import json


def Update():
    url = "https://raw.githubusercontent.com/Dashtiss/Lightning-MC-Bot/master/saves.json"
    response = requests.get(url)
    with open("saves.json", "w") as SavesFile:
        json.dump(response.json(), SavesFile)
    del response
    url = "https://raw.githubusercontent.com/Dashtiss/Lightning-MC-Bot/master/Bot.py"
    response = requests.get(url)

    if os.path.exists("Bot.py"):
        with open("Bot.py", "r", encoding="utf-8") as BotFile:
            bot = BotFile.read()
        if bot != response.text:
            print("Updating Bot")
            with open("Bot.py", "w", encoding="utf-8") as BotFile:
                BotFile.write(response.text)
            import Bot
            Bot.Run()
        else:
            print("Bot is un up date")
    else:
        with open("Bot.py", "w", encoding="utf-8") as BotFile:
            BotFile.write(response.text)
            import Bot
            Bot.Run()


if __name__ == "__main__":
    Update()
