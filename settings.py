import pathlib
from dotenv import load_dotenv
import os

lastNumber = 0
HighestNumber = 0
lastUsers = ""
UsersButtonPushed = {}
CTOnline = False


def updateScore(User: str, Number: int):
    global lastNumber, lastUsers
    lastNumber = Number
    lastUsers = User


def UpdateHighest(NewNumber: int):
    global HighestNumber
    HighestNumber = NewNumber


BASE_DIR = pathlib.Path(__file__).parent

cogs_dir = BASE_DIR / "cogs"
