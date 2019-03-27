GIT_REPO_PATH = ''
GIT_REPO_BRANCH = 'master'


GOOGLE_USERNAME = ''
GOOGLE_PASSWORD = ''
GOOGLE_LOCALE = 'en_US'
GOOGLE_DEVICE_ID = ''


GPM_TRACK_FIELDS = [
    'title', 'artist', 'album'
]


import csv
import os
import sys

from gmusicapi import Mobileclient as GpmClient

from git import Repo as GitRepo
from git.exc import InvalidGitRepositoryError, NoSuchPathError


def git_initialise():
    try:
        # attempt to open existing repository
        repository = GitRepo(GIT_REPO_PATH)
        print(f"Opened existing repository in '{GIT_REPO_PATH}'")
    except (InvalidGitRepositoryError, NoSuchPathError):
        # initialise bare repository
        os.makedirs(GIT_REPO_PATH, exist_ok=True)
        repository = GitRepo.init(GIT_REPO_PATH)
        print(f"Initialised new repository in '{GIT_REPO_PATH}'")
    
    return repository


def git_clean_repo(repository):
    # check if repository is dirty
    if repository.head.is_valid():
        if repository.is_dirty():
            print("Repository is dirty")
            print("Attempting hard reset to HEAD")
            repository.head.reset(working_tree=True)
            print("Hard reset successful")


def git_checkout(repository):
    # check for requested branch
    if repository.active_branch.name != GIT_REPO_BRANCH:
        print(f"HEAD is on branch '{repository.active_branch.name}'")
        print(f"Checking out branch '{GIT_REPO_BRANCH}'")
        repository.git.checkout('-b', GIT_REPO_BRANCH)
        print("Checked out requested branch")


def git_changes_made(repository):
    return repository.is_dirty() or len(repository.index.diff(None))


def gpm_initialise():
    return GpmClient(debug_logging=True)


def gpm_authenticate(client):
    print("Attempting to authenticate with Google Play Music")

    client.login(
        GOOGLE_USERNAME,
        GOOGLE_PASSWORD,
        GOOGLE_DEVICE_ID,
        locale=GOOGLE_LOCALE
    )

    return client.is_authenticated()

def gpm_build_track_cache(tracks):
    return {track['id']:track for track in tracks}


def gpm_build_track_entry(track):
    return {
        'title': track.get('title', ''),
        'artist': track.get('artist', ''),
        'album': track.get('album', '')
    }


def gpm_build_playlist_file_name(name):
    return name.replace('/', '-') + '.csv'


def gpm_get_playlists(client):
    return sorted(
        client.get_all_user_playlist_contents(),
        key=lambda playlist: playlist['name']
    )


def gpm_get_tracks(client):
    return client.get_all_songs()


def gpm_resolve_track(entry, cache):
    if 'track' in entry:
        return entry['track']
    elif 'trackId' in entry:
        if entry['trackId'] in cache:
            return cache[entry['trackId']]

    return None


def main():
    # git initialisation
    repository = git_initialise()
    git_clean_repo(repository)
    git_checkout(repository)


    # gpm initialisation
    client = gpm_initialise()
    if not gpm_authenticate(client):
        print('Authentication failed.')
        sys.exit(1)

    # gpm api calls
    playlists = gpm_get_playlists(client)
    tracks = gpm_get_tracks(client)

    # build gpm track cache
    cache = gpm_build_track_cache(tracks)


    # playlist diffs
    diffs = []


    # iterate through playlists
    for playlist in playlists:
        # build file name + path
        file_name = gpm_build_playlist_file_name(playlist['name'])
        file_path = os.path.join(GIT_REPO_PATH, file_name)
        
        # create / open playlist file for writing
        with open(file_path, 'w', newline='') as csv_file:
            print('Exporting playlist "' + playlist['name'] + '"... ')

            # write CSV file header
            csv_writer = csv.DictWriter(csv_file, GPM_TRACK_FIELDS)
            csv_writer.writeheader()

            # iterate through playlist entries
            for entry in playlist['tracks']:
                # resolve track entry, build output
                track = gpm_resolve_track(entry, cache)
                output = gpm_build_track_entry(track)

                # write track output to disk
                if track is not None:
                    csv_writer.writerow(output)

                
            print('\tWritten to disk.')

        # calculate playlist diff
        diff = repository.index.diff(None, create_patch=True, paths=file_path)

        # check for tracking status
        changed = bool(len(diff))
        untracked = file_name in repository.untracked_files

        # check for playlist changes
        if changed:
            # append to global diffs list
            print('\tCalculating diff...')
            diffs += diff
            print('\tDiff appended.')

        # check for committable diff
        if changed or untracked:
            # stage playlist file
            print('\tStaging "' + file_path + '"... ')
            repository.index.add([file_path])
            print('\tStaged.')


    # check for playlist changes
    if git_changes_made(repository):
        # commit staged playlist changes
        print('Committing to repository... ', end='')
        repository.index.commit('Playlist changes')
        print('done!')
    else:
        print('No diff to commit.')
        return

main()