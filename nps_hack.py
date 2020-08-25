import requests
import json
import time
import subprocess

def _get_number_of_available_day_passes_on_given_day(year, month, day):
    '''Returns the number of yosemite available day passes on a given day of the year.

    Arguments:
        year (str): The year, ie, 2020
        month (str): The month, ie, 09
        day (str): The day, ie, 04
    '''
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    response = requests.get(
        f'https://www.recreation.gov/api/ticket/availability/facility/300015/monthlyAvailabilitySummaryView?year={year}&month={month}&inventoryBucket=FIT',
        headers={'user-agent': user_agent}
    )

    try:
        response.raise_for_status()
    except:
        applescript = """
        display dialog "Error fetching nps data." ¬
        with title "Check the day pass scripts" ¬
        with icon caution ¬
        buttons {"OK"}
        """

        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
        raise

    dates_json = json.loads(response.text)

    return dates_json['facility_availability_summary_view_by_local_date'][f'{year}-{month}-{day}']['tour_availability_summary_view_by_tour_id']['3000']['reservable']

def notify_when_day_pass_is_available(year, month, day):
    counter = 0
    while _get_number_of_available_day_passes_on_given_day(year, month, day) == 0:
        counter += 1
        print(f'Still unavailable on {year}, {month}, {day}. Trying again... attempt #{counter}')
        # Check every 5 minutes
        time.sleep(300)

    print(f'Day passes are available on {year}, {month}, {day}')

    applescript = """
    display dialog "Yosemite day pass available, check the dates you wanted." ¬
    with title "Day pass" ¬
    with icon caution ¬
    buttons {"OK"}
    """

    subprocess.call("osascript -e '{}'".format(applescript), shell=True)


# Replace this with the dates you want
# Simply save this file somethere on your Apple computer and run "python nps_hack.py"
# You might need install Anaconda python in order to run this since it uses the "requests" module above.
notify_when_day_pass_is_available('2020', '09', '04')
