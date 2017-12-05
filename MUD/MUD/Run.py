import time

from Server import Server
from LeitorJSON import LeitorJSON

def main():
    rooms = LeitorJSON("Rooms.json").carregarJson()   
    Server(rooms, time.time()).start()

main()