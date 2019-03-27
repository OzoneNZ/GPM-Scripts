# GPM Dump Scripts

Collection of helper scripts to extract playlists from Google Play Music:

* **gpm_devices_dump.py**: dumps a list of devices registered against your Google Play Music account
* **gpm_playlist_dump.py**: dumps all playlists to CSV files and commits changes to a Git repository


## Environment set-up

1. You'll need to install these:

* [Python 3](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

2. Then you'll need to install the Python 3 packages required by the scripts:

* [`pip3 install gmusicapi`](https://pypi.org/project/gmusicapi/)
* [`pip3 install GitPython`](https://pypi.org/project/gitpython/)

3. Initialise an empty Git repository somewhere on your disk by either:

* Using the command line: `git init .`
* Using a Git application like the [GitHub App](https://desktop.github.com/) to do it.


## Devices dump script
### Required before using `gpm_playlist_dump.py`

1. Open the `gpm_devices_dump.py` script with a text editor and change `GOOGLE_USERNAME` / `GOOGLE_PASSWORD` to match your Google account credentials.

2. Save your changes and run the `gpm_devices_dump.py` script (from the command line: `python3 gpm_devices_dump.py`)

3. Read over the devices list and pick one you actively use:

```
[{'friendlyName': 'ONEPLUS A5000',
  'id': '0x1234567891234567',
  'kind': 'sj#devicemanagementinfo',
  'lastAccessedTimeMs': '1535005522344',
  'type': 'ANDROID'}]
```
  
In this case, I'm using my OnePlus 5 with a device ID of `0x1234567891234567`. Remove the `0x` prefix if present, and copy this value to your clipboard.


## Playlist dump script

1. Open the `gpm_playlist_dump.py` script with a text editor and change `GOOGLE_USERNAME` / `GOOGLE_PASSWORD` to match your Google account credentials.

2. Change `GOOGLE_DEVICE_ID` to match the device ID you found from `gpm_devices_dump.py`.

3. Change `GIT_REPO_PATH` to point to your blank Git repository. Optionally, you can change `GIT_REPO_BRANCH` as well but you will need to create + checkout the non-master branch yourself.

4. Save your changes and run the `gpm_playlist_dump.py` script (from the command line: `python3 gpm_playlist_dump.py`)

You'll see a whole heap of console output similar to this:

```
blake at Blakes-MacBook-Pro in ~/Desktop                                                                                                                                                                                              9:10
> python3 gpm_playlist_dump.py
Initialised new repository in '/Users/Blake/Desktop/TestRepo'
Attempting to authenticate with Google Play Music
Exporting playlist "2015"...
        Written to disk.
        Staging "/Users/Blake/Desktop/TestRepo/2015.csv"...
        Staged.
```


