GOOGLE_USERNAME = ''
GOOGLE_PASSWORD = ''
GOOGLE_LOCALE = 'en_US'


import sys

from gmusicapi import Mobileclient as GpmClient
from pprint import pprint


def gpm_initialise():
    return GpmClient(debug_logging=True)


def gpm_authenticate(client):
    print("Attempting to authenticate with Google Play Music")

    client.login(
        GOOGLE_USERNAME,
        GOOGLE_PASSWORD,
        GpmClient.FROM_MAC_ADDRESS,
        locale=GOOGLE_LOCALE
    )

    return client.is_authenticated()


def gpm_get_devices(client):
    return client.get_registered_devices()


def main():
    # gpm initialisation
    client = gpm_initialise()
    if not gpm_authenticate(client):
        print('Authentication failed.')
        sys.exit(1)

    devices = gpm_get_devices(client)
    pprint(devices)


main()