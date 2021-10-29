# Author: Kyler Burnett
# Date: 10/29/2021

# Notes:
# Root location to check for latest version.
# https://github.com/yt-dlp/yt-dlp/releases/download/2021.10.22/yt-dlp.exe

# USAGE
# Install the requirements.txt: pip install -r requirements.txt
# Either use this script directly, or import it into an existing python script like so:
# from youtubedlchecker import getLatestYoutubeDlVersion
# resultLocation = getLatestYoutubeDlVersion()

import requests
import os
import re

# Set downloadPath to the directory where you want youtube-dl.exe to be downloaded to.
downloadPath = "C:/Users/user/Downloads/gohere"
githubDownloadsLatest = "https://github.com/yt-dlp/yt-dlp/releases/latest"
downloadRegex = r"https://github.com/yt-dlp/yt-dlp/releases/download/\d+\.\d+\.\d+/yt-dlp.exe"
currentVersionFileName = "current_version.txt"


def downloadFile(downloadPath, url):
    print("Downloading new exe...")
    fileName = os.path.join(downloadPath, url.split("/")[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fileName, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print("Download complete!\n youtube-dl.exe downloaded to: " + downloadPath)
    return fileName

def getLatestVersion():
    print("Checking github project for the latest yt-dlp.exe version...")
    downloadsPage = requests.get(githubDownloadsLatest)
    url = re.search(downloadRegex, downloadsPage)[0]
    
    if url:
        print("Found url: {0}".format(url))
        siteVersion = url.split("/download/")[1].split("/yt-dlp.exe")[0]

        currentVersion = ""
        # Create current_version.txt if it does not already exist.
        if not os.path.isfile(currentVersionFileName):
            file = open(currentVersionFileName, "w+").close()
        else:
            with open(currentVersionFileName, "r") as f:
                currentVersion = f.read().replace("\n", "")

        if siteVersion != currentVersion:  # It's a new version folks.
            print("A new version of youtube-dl.exe was found!")
            # Write new version to file.
            with open(currentVersionFileName, "w+") as f:
                f.write(siteVersion)

            downloadFile(downloadPath, url)

            return os.path.join(downloadPath, "yt-dlp.exe")
        else:
            alreadyExistsMsg = "Already on latest version of yt-dlp.exe\n\nEnd of Line."
            print(alreadyExistsMsg)
            return(alreadyExistsMsg)
    else:
        print("Error, yt-dlp.exe url not found on page.")

if __name__ == '__main__':
   getLatestVersion()
