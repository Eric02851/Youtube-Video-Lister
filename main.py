import requests
import re

def writeFile(inputStr):
    f = open("dumpFile.txt", "w")
    f.write(inputStr)
    f.close()

def getPlaylistPage(playlistUrl):
    return requests.get(playlistUrl).text

def getPlaylistId_totalVideos(response):
    playlistIndex = response.find(r"\u0026list=") + 11
    playlistId = response[playlistIndex : playlistIndex + 24]

    totalVideosIndexStart = response.find('"totalVideos"') + 14
    totalVideosIndexEnd = response.find(',', totalVideosIndexStart)
    totalVideos = int(response[totalVideosIndexStart : totalVideosIndexEnd])

    return playlistId, totalVideos

def takeSecond(elem):
    return elem[1]

def getIndexs(response, playlistId, sortList):
    indexNumbers = []
    sortedIndexs = []
    indexPositions = [m.start() for m in re.finditer("index=", response)]

    writeFile(response)

    for i in range(len(indexPositions)):
        index = response[indexPositions[i] : indexPositions[i] + 9]
        stripped = int(re.sub('[^0-9]','', index))

        if stripped not in sortList and rf"u0026list={playlistId}\u0026" in response[indexPositions[i] - 40 : indexPositions[i]]:
            sortList.append(stripped)
            sortedIndexs.append((indexPositions[i], stripped))

    sortedIndexs.sort(key=takeSecond)
    return sortedIndexs, sortList

def getVideoIds(response, indexList, videoIdList):
    for i in indexList:
        if response[i[0] - 52 : i[0] - 41] not in videoIdList:
            videoIdList.append(response[i[0] - 52 : i[0] - 41])

    return videoIdList

def main():
    sortList = []
    videoIdList = []

    playlistUrl = "https://www.youtube.com/playlist?list=UUBa659QWEk1AI4Tg--mrJ2A&playnext=1&index=1"
    response = getPlaylistPage(playlistUrl)

    playlistId, totalVideos = getPlaylistId_totalVideos(response)

    indexList, sortList = getIndexs(response, playlistId, sortList)
    videoIdList = getVideoIds(response, indexList, videoIdList)
    print(len(videoIdList))

    while len(videoIdList) < totalVideos:
        playlistUrl = rf"https://www.youtube.com/watch?v={videoIdList[-1]}&list={playlistId}&index={indexList[-1][1]}"
        print(playlistUrl)
        response = getPlaylistPage(playlistUrl)

        indexList, sortlist = getIndexs(response, playlistId, sortList)
        videoIdList = (getVideoIds(response, indexList, videoIdList))
        print(len(videoIdList))

    print(videoIdList)

main()