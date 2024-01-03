import requests
import os


def Update():
    url = "https://raw.githubusercontent.com/Dashtiss/Lightning-MC-Bot/master/Bot.py"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve file. Status code: {response.status_code}")
        return None


if __name__ == "__main__":
    update = Update()
    if update is None:
        raise "File is Error"
    if os.path.exists("Bot.py"):
        with open("Bot.py", "r", encoding="utf-8") as BotFile:
            bot = BotFile.read()
        if bot != update:
            print("Updating Bot")
            with open("Bot.py", "w", encoding="utf-8") as BotFile:
                BotFile.write(update)
            import Bot
            Bot.Run()
        else:
            print("Bot is un up date")
    else:
        with open("Bot.py", "w", encoding="utf-8") as BotFile:
            BotFile.write(update)
            import Bot
            Bot.Run()
