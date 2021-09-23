import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
                      no month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    cities = list(CITY_DATA.keys())
    city = ""

    # get city filter
    while city not in cities:
        city = input("Which city's data would you like to explore? Please " \
        "choose from (Chicago, New York City, Washington)\n>> ").lower()
        print()

        if city not in cities:
            print("Did you enter a valid city name? Please check your input " \
            "and try again.\n")

    # get month filter if any
    month = ""
    while month not in MONTHS + ['all']:
        month = input("Which month's data would you like to explore? " \
        "Enter a month between January and June. If you wish to view all " \
        "months' data, type ALL.\n>> ").lower()
        print()
        break

        if month not in MONTHS + ['all']:
            print("Did you enter a valid month? Please check your input " \
            "and try again.\n")

    # get day filter if any
    day = ""
    while day not in DAYS + ['all']:
        day = input("Which day of the week's data would you like to explore? " \
        "Enter a day (Monday, Tuesday, etc.) If you wish to view all " \
        "days' data, type ALL.\n>> ").lower()
        print()

        if day not in DAYS + ['all']:
            print("Did you enter a valid day? Please check your input " \
            "and try again.\n")

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day
    if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or
                      "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to
                    apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if applicable
    if month == 'all':
        most_comm_month = MONTHS[df['month'].mode()[0] - 1].title()
        print(f'Most common month: {most_comm_month}')
    else:
        print("If you wish to see most common month in the dataset, choose " \
        "ALL when asked to choose a month\n")

    # display the most common day of week if applicable
    if day == 'all':
        most_comm_day = df['day_of_week'].mode()[0]
        print(f'Most common day: {most_comm_day}')
    else:
        print("If you wish to see most common day in the dataset, choose " \
        "ALL when asked to choose a day\n")

    # display the most common start hour
    most_comm_hour = df['hour'].mode()[0]
    print(f'Most common hour: {most_comm_hour}:00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_comm_start_stat = df['Start Station'].mode()[0]
    print(f'Most commonly used start station was {most_comm_start_stat}')

    # display most commonly used end station
    most_comm_end_stat = df['End Station'].mode()[0]
    print(f'Most commonly used end station was {most_comm_end_stat}')

    # display most frequent combination of start station and end station trip
    start_and_end = ('from ' + df['Start Station'] + ' to ' + \
    df['End Station']).mode()[0]
    print(f'Most common combination is {start_and_end}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = datetime.timedelta(seconds=int(df['Trip Duration'].sum()))
    print(f'Total travel time: {tot_travel_time}')

    # display mean travel time
    mean_travel_time = datetime.timedelta(seconds=int(df['Trip Duration'].mean()))
    print(f'Average trip duration: {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_counts = df['User Type'].value_counts()
    print(f"Numbers of each user type:\n{user_counts.to_string()}\n")

    # display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"Numbers of each gender:\n{gender_counts.to_string()}\n")
    else:
        print("Gender data is available for Chicago and New York City")

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_comm_birth_year = int(df['Birth Year'].mode()[0])
        print(f'Earliest birth year is {earliest_birth_year}')
        print(f'Most recent birth year is {most_recent_birth_year}')
        print(f'Most common birth year is {most_comm_birth_year}')
    else:
        print("Birth year data is available for Chicago and New York City")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nEnter y to restart or anything else to exit.\n')
        print()
        if restart.lower() != 'y' and restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
