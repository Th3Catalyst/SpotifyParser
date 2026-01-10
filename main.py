import json
import time

from terminalMenu import newMenu
import math
from datetime import datetime

def main() -> None:
    while True:
        pathToData: str = input("Enter path to data folder: ")
        try:
            with open(pathToData + r"\Marquee.json", "r", errors='ignore') as file:
                data: list[dict] = json.load(file)
            with open(pathToData + r"\StreamingHistory_music_1.json", "r", errors='ignore') as file:
                data: list[dict] = json.load(file)
            break
        except FileNotFoundError:
            print("Incorrect path, listening history not found in folder.")
    while True:
        startDateStr: str = input("Enter start date (YYYY-MM-DD), leave blank for earliest date: ")
        try:
            if startDateStr == "":
                startDate: datetime = datetime(1, 1,1)
                break
            startDate: datetime = datetime.strptime(startDateStr, "%Y-%m-%d")
            break
        except ValueError:
            print(f"Incorrect format, '{startDateStr}' is not in the form YYYY-MM-DD.")

    with open(fr"{pathToData}\StreamingHistory_music_1.json", "r", encoding="utf-8") as history2, open(fr"{pathToData}\StreamingHistory_music_0.json", "r", encoding="utf-8") as history, open(fr"{pathToData}\Marquee.json", "r", encoding="utf-8") as artistsF:
        data = json.load(history)
        data2 = json.load(history2)
        data.extend(data2)
        artists: list[dict] = json.load(artistsF)

        artistMode = newMenu(["All artists", "One artist"])
        time.sleep(0.2)
        if artistMode == "One artist":
            artistList: list = [artist["artistName"] for artist in artists]
            artist = newMenu(artistList)
            artistData: dict[str, list[int | float]] = {}
            for song in data:
                if datetime.strptime(song["endTime"].split(" ")[0], "%Y-%m-%d") < startDate: continue
                if song["artistName"] == artist and song["msPlayed"] > 30000:
                    if song["endTime"].split(" ")[0] not in artistData:
                        artistData[song["endTime"].split(" ")[0]] = [0, 0]
                    artistData[song["endTime"].split(" ")[0]][0] += song["msPlayed"]
                    artistData[song["endTime"].split(" ")[0]][1] += 1

            totalTime: float = 0
            totalSongs: int = 0
            for date, info in artistData.items():
                totalTime += info[0]
                totalSongs += info[1]
                hours = round(info[0] / (1000 * 60 * 60))
                minutes = round((info[0] / (1000 * 60 * 60) - math.floor(info[0] / (1000 * 60 * 60))) * 60, 2)
                print(f"{date}:", hours, "hours,", minutes, "minutes, with", info[1], "songs")

            totalHours = round(totalTime / (1000 * 60 * 60))
            totalMinutes = round((totalTime / (1000 * 60 * 60) - math.floor(totalTime / (1000 * 60 * 60))) * 60, 2)
            print(f"Since {next(iter(artistData))}, you listened to {artist} for a total of {totalHours} hours and {totalMinutes} minutes, and listened to {totalSongs} songs (including duplicates).")
        elif artistMode == "All artists":
            artistData: dict[str, list[int | float]] = {}
            for song in data:
                if datetime.strptime(song["endTime"].split(" ")[0], "%Y-%m-%d") < startDate: continue
                if song["msPlayed"] > 30000:
                    if song["endTime"].split(" ")[0] not in artistData:
                        artistData[song["endTime"].split(" ")[0]] = [0, 0]
                    artistData[song["endTime"].split(" ")[0]][0] += song["msPlayed"]
                    artistData[song["endTime"].split(" ")[0]][1] += 1

            totalTime: float = 0
            totalSongs: int = 0
            for date, info in artistData.items():
                totalTime += info[0]
                totalSongs += info[1]
                hours = round(info[0] / (1000 * 60 * 60))
                minutes = round((info[0] / (1000 * 60 * 60) - math.floor(info[0] / (1000 * 60 * 60))) * 60, 2)
                print(f"{date}:", hours, "hours,", minutes, "minutes, with", info[1], "songs")

            totalHours = round(totalTime / (1000 * 60 * 60))
            totalMinutes = round((totalTime / (1000 * 60 * 60) - math.floor(totalTime / (1000 * 60 * 60))) * 60, 2)
            print(f"Since {next(iter(artistData))}, you listened on Spotify for a total of {totalHours} hours and {totalMinutes} minutes, and listened to {totalSongs} songs (including duplicates).")
        else:
            raise ValueError("How did we get here?")

if __name__ == "__main__":
    main()