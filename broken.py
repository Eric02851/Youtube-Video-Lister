from requests import get
from re import finditer

def getVideoIds():
    response = get("https://www.youtube.com/playlist?list=PUrzfYhLjOkfAcmjixeeiEnQ&playnext=1&index=1").text
    videoIdPositions = [m.start() for m in finditer('"videoId"', response)]
    videoIds = []
    for i in range(len(videoIdPositions)):
        videoIds.append(response[videoIdPositions[i] + 11 : videoIdPositions[i] + 22])
    return videoIds

def getPastebinUrls(videoIds):
    pastebinUrls = []
    for i in videoIds:
        response = get(f"http://www.youtube.com/watch?v={i}").text
        position = response.find("https://pastebin.com")
        print(f"http://www.youtube.com/watch?v={i} : {position}")

        if position != -1:
            
            pastebinUrls.append(response[position : position + 29])

    return pastebinUrls

def main():
    videoIds = getVideoIds()
    print(len(videoIds))
    #pastebinUrls = getPastebinUrls(videoIds)
    #print(pastebinUrls)

main()