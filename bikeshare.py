import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city!="chicago" and city!="new york city" and city!="washington":
        city=input("Would you like to see data for Chicago, New york, or Washington?").strip().lower()
        if city!="chicago" and city!="new york city" and city!="washington":
            print("Invalid city!! Please enter either 'Chicago', 'New York City', or 'Washington'.\n")


    # TO DO: get user input for month (all, january, february, ... , june)
    valid_months = ['january','february','march','april','may','june']
    month=""
    while month not in valid_months and month!="all":
        month = input("Which Month?").lower()
        if month not in valid_months and month!="all":
            print("Invalid month!! \n")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day=""
    while day not in day_of_week and day!="all":
        day = input("Which Day?").lower()
        if day not in day_of_week and day!="all":
            print("Invalid day!! \n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    print(df)
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    df['End Time'] = pd.to_datetime(df['End Time'])

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month.lower()) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour'] = df['Start Time'].dt.hour

    # TO DO: display the most common month
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        print("The most common month is: {}".format(months[most_common_month-1]))

    # TO DO: display the most common day of week
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        print("The most common day is: {}".format(most_common_day))

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour is: {}".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""


    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is: {}".format(most_common_start_station))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is: {}".format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'] + "--TO--" + df['End Station']
    most_common_start_end_station = df['Start To End'].mode()[0]
    print("The most common start to end trip is: {}".format(most_common_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum(skipna=True)
    mean_travel_time = df['Trip Duration'].mean(skipna=True)

    print(f"Total Travel Time: {total_travel_time}")
    print(f"Mean Travel Time: {mean_travel_time}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)



def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("The count of user types is as follows: ")
    for index, val in user_type_count.head(2).items():
        print("{} : {}".format(index,val))

    print('-' * 40)

    # TO DO: Display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print("The count of each gender is as follows: ")
        for index, val in gender_count.head(2).items():
            print("{} : {}".format(index, val))

    print('-' * 40)

    # TO DO: Display earliest, most recent, and most common year of birth
    try:

        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print(" The earliest year of birth is: {} \n The most recent year of birth is: {} \n The most common year of birth is: {}".format(int(earliest_birth_year),int(most_recent_birth_year),int(most_common_birth_year)))

    except KeyError:
        print("Year of birth not available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """
    Displays raw data in chunks of 5 rows upon user request.

    Args:
        df (DataFrame): The filtered dataset.
    """
    cnt = 0
    while True:
        display_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no:\n").strip().lower()
        if display_data != 'yes':
            break
        print(df.iloc[cnt:cnt+5])
        cnt += 5



def main():
    """
       Main driver function to run the bikeshare analysis script.
       """

    while True:
        city, month, day = get_filters()
        print(city,month,day)
        df = load_data(city, month, day)
        show_raw_data(df)
        time_stats(df,month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
