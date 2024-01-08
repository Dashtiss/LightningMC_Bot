import os
import shutil
import pathlib


def Update():
    url = "https://github.com/Dashtiss/LightningMC_Bot"
    repo_path = pathlib.Path(__file__).parent / "LightningMC_Bot"

    if os.path.exists(repo_path):
        # Import and run the Bot
        try:
            os.system(f"python {pathlib.Path(__file__).parent}/LightningMC_Bot/Bot.py")
        except KeyboardInterrupt:
            exit(1)
        except Exception as e:
            print(f"Error while importing and running the Bot: {e}")
    else:
        # Clone the repository again
        os.system(f"git clone {url}")
        # Import and run the Bot
        try:
            os.system(f"python {pathlib.Path(__file__).parent}/LightningMC_Bot/Bot.py")
        except KeyboardInterrupt:
            exit(1)
        except Exception as e:
            print(f"Error while importing and running the Bot: {e}")


if __name__ == "__main__":
    Update()
