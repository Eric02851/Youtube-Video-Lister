import requests
import re

def getPlaylistPage(playlistUrl):
    return requests.get(playlistUrl).text

def getPlaylistId_totalVideos(response):
    totalVideosIndexStart = response.find('"totalVideos"') + 14
    totalVideosIndexEnd = response.find(',', totalVideosIndexStart)
    totalVideos = int(response[totalVideosIndexStart : totalVideosIndexEnd])

    return totalVideos

def takeSecond(elem):
    return elem[1]

def getIndexs(response, playlistId, sortList):
    indexNumbers = []
    sortedIndexs = []
    indexPositions = [m.start() for m in re.finditer("index=", response)]

    for i in range(len(indexPositions)):
        index = response[indexPositions[i] + 6 : response.find('"', indexPositions[i])]

        if index not in sortList and rf"u0026list={playlistId}\u0026" in response[indexPositions[i] - 40 : indexPositions[i]] and index.isdigit() == True:
            sortList.append(index)
            sortedIndexs.append((indexPositions[i], index))

    sortedIndexs.sort(key=takeSecond)
    return sortedIndexs, sortList

def getVideoIds(response, indexList, videoIdList):
    for i in indexList:
        if response[i[0] - 52 : i[0] - 41] not in videoIdList:
            videoIdList.append(response[i[0] - 52 : i[0] - 41])

    return videoIdList

def getPlaylist(channelId):
    response = requests.get(f"https://www.youtube.com/channel/{channelId}/videos").text
    index = response.find("list=")
    playlistId = response[index + 5 : index + 29]

    return f"https://www.youtube.com/playlist?list={playlistId}&playnext=1&index=1", playlistId

def main(channelId):
    sortList = []
    videoIdList = []

    playlistUrl, playlistId = getPlaylist(channelId)
    response = getPlaylistPage(playlistUrl)
    print(playlistUrl)

    totalVideos = getPlaylistId_totalVideos(response)

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
    print(len(videoIdList))
    
    with open('videoIds.txt', 'w') as f:
        for item in videoIdList:
            f.write("%s\n" % item)

main("UCBa659QWEk1AI4Tg--mrJ2A")