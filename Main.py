import os
import shutil


def Update():
    url = "https://github.com/Dashtiss/LightningMC_Bot"
    shutil.rmtree("LightningMC_Bot")
    os.system(f"git clone {url}")
    from LightningMC_Bot import Bot

    Bot.Run()


if __name__ == "__main__":
    Update()
