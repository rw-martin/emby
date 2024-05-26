# Emby Media Management
This project provides a script for analyzing media content stored in Emby, a media server solution. It includes functionality to fetch user information, calculate media file sizes, and display media details with formatted output.

![output](/screenshots/script-output.png "output")

## Features

- Fetch users from the Emby server.
- Calculate the size of media files tßat have past a defined age threshold
- Format and display the output
- Display a table with media details, including series, season, episode, date created, size, and age.

### Prerequisites
- Python 3.6 or higher
- `pip` (Python package installer)

### Dependencies

The project requires the following Python packages:

- `embyapi`
- `prettytable`
- `python-dateutil`

You can install the required packages using the following command:

```bash
pip install embyapi prettytable python-dateutil