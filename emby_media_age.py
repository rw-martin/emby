#from __future__ import print_function
import datetime
import embyapi
import config
from embyapi.rest import ApiException
from prettytable import PrettyTable
from dateutil.relativedelta import relativedelta

# ANSI escape codes for coloring
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Configure API key authorization: apikeyauth
configuration = embyapi.Configuration()
configuration.api_key['api_key'] = config.embyKey
configuration.host = config.embyHost

# Create an instance of the required Emby API classes
api_client = embyapi.ApiClient(configuration)
user_api = embyapi.UserServiceApi(api_client)
items_api = embyapi.ItemsServiceApi(api_client)

def get_all_users():
    try:
        users = user_api.get_users()
        return users
    except ApiException as e:
        print(f"Exception when calling UserServiceApi->get_users: {e}\n")
        return []

def get_file_size(media):
    try:
        return media._media_sources[0].size / 1e9  # Size in gigabytes
    except (IndexError, AttributeError):
        return 0  # Handle cases where media_sources or size might not be available

def format_elapsed_time(date_created, current_date):
    delta = relativedelta(current_date, date_created)
    years = f"{delta.years:02}yrs"
    months = f"{delta.months:02}mths"
    days = f"{delta.days:02}days"
    age = f"{years} {months} {days}"
    if (delta.years*12)+delta.months >= config.threshold:
        return f"{Colors.FAIL}{age}{Colors.ENDC}"
    else:
        return age

def get_emby_media():
    try:
        users = get_all_users()
        if not users:
            print("No users found.")
            return

        total_size = 0
        item_count = 0
        current_date = datetime.datetime.now(datetime.timezone.utc)
        table = PrettyTable()
        table.field_names = ["Item", "Series", "Season", "Episode", "Date Created", "Size", "Age"]

        all_media = items_api.get_users_by_userid_items(
            user_id=users[0].id, recursive=True, include_item_types='Episode',
            fields="DateCreated,Size,MediaStreams", sort_by='DateCreated'
        )

        for media in all_media.items:
            if not media.user_data.played:
                title = media.name or media.original_title or media.sort_name or "Unknown Title"
                size = get_file_size(media)
                item_count += 1
                formatted_size = f"{size:.2f} g" if size else "Unknown Size"
                total_size += size
                age = format_elapsed_time(media.date_created, current_date)
                table.add_row([item_count, media.series_name, media.season_name, title, media.date_created.strftime('%Y-%m-%d %H:%M:%S'), formatted_size, age])

        print(f"{Colors.OKGREEN}Total footprint on disk: {item_count} media files @ {total_size:.2f} g{Colors.ENDC}")
        print(table)

    except ApiException as e:
        print(f"Exception when calling API: {e}\n")

if __name__ == "__main__":
    get_emby_media()