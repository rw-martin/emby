# Emby Media Management
This project leverages the Emby server API to analyze stored content to determine which TV episodes have not been watched since being downloaded. Anything over a defined date threshold is highlighted in RED.

![output](/screenshots/script-output.png "output")

## Features

- Fetch users from the Emby server.
- Calculate the size of media files that have aged past a defined threshold
- Display a table with media details, including series, season, episode, date created, size, and media age since download.

### Prerequisites
- Python 3.6 or higher

### Dependencies

The project requires the following Python packages:

- `embyapi` # v4.1.1.0a0
- `prettytable` # v3.10.0
- `python-dateutil` # v2.9.0.post0

You will need a regular Python module named config.py that contains the following where you need to replace the API KEY and SERVER w/ values relevant to your setup:
- embyKey='<EMBY SERVER API KEY>'
- embyHost='https://<EMBY SERVER>/emby'
- threshold = 18  # number of months