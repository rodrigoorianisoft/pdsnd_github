'''
Statistics Computed
    You will learn about bike share use in Chicago, New York City, and Washington by computing a variety of descriptive statistics. In this project, you'll write code to provide the following information:

#1 Popular times of travel (i.e., occurs most often in the start time)
    most common month
    most common day of week
    most common hour of day

#2 Popular stations and trip
    most common start station
    most common end station
    most common trip from start to end (i.e., most frequent combination of start station and end station)

#3 Trip duration
    total travel time
    average travel time

#4 User info
    counts of each user type
    counts of each gender (only available for NYC and Chicago)
    earliest, most recent, most common year of birth (only available for NYC and Chicago)

ref:
    https://pandas.pydata.org/pandas-docs/version/0.22/api.html#
    https://pandas.pydata.org/pandas-docs/version/0.22/api.html#datetimelike-properties
    https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.to_datetime.html#pandas.to_datetime
    https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.Series.sort_values.html#pandas.Series.sort_values
    https://docs.python.org/3/library/statistics.html
    https://docs.python.org/3/library/json.html


'''

import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def to_json(d):
    '''
    Just to prettify the output printing

    Return a json with identation
    '''
    dic_str = {}

    for k in d.keys():
        dic_str[k] = str(d[k]) #typecasting to string because I've got some issues with int64 and float point serialization

    return json.dumps(dic_str, indent=4)

def get_input_as_int(input_text, min, max):
    '''
    To validate the input values (all inout options must be an int value)

    Return an int value between min and max parameters
    '''
    while True:
        try:
            result = int(input(input_text + ' '))
            
            if not(min <= result <= max):
                print("Incorrect value.")
                continue
            
            return result

        except ValueError:
            print("Incorrect value. That's not an int!")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*40)
    print('\n\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    
    city = get_input_as_int('Would you like to see data for 1=Chicago, 2=New York, or 3=Washington?', 1, 3)

    city = list(CITY_DATA.keys())[city-1] #retrieve the dictionary key by "index"

    month = None
    day = None
    
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    time = get_input_as_int('Would you like to filter the data by 1=month, 2=day, 3=both, or 0=not at all?', 0, 3)

    if time == 3 or time == 1:
        month = get_input_as_int('Wich month? 1=January, 2=February, 3=March, 4=April, 5=May, or 6=June?', 1, 6)        
    
    if time == 3 or time == 2:
        day = get_input_as_int('Wich day? 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday, or 7=Sunday?', 1, 7) - 1

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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #new indexes to support some calculations
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['weekday_name'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month:
        df = df[df['month'] == month]

    if day:
        df = df[df['weekday'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0]

    # display the most common day of week
    day_of_week = df['weekday_name'].mode()[0]

    # display the most common start hour
    start_hour = df['hour'].mode()[0]

    result = {'month': month,
              'day of week': day_of_week,
              'start hour': start_hour}

    print(to_json(result))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    # formating the outputs
    fmt = lambda s: '{} ({})'.format(s.index[0], s.iloc[0])
    fmt2 = lambda s: '{} -> {} ({})'.format(s.index[0][0], s.index[0][1], s.iloc[0])

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = fmt(df['Start Station'].value_counts())
    
    # TO DO: display most commonly used end station
    end_station = fmt(df['End Station'].value_counts())

    # display most frequent combination of start station and end station trip
    station_to_station = fmt2(df.groupby(['Start Station', 'End Station'])['Start Time'].count().sort_values().tail(1))

    result = {'start station': start_station,
              'end station': end_station,
              'station to station': station_to_station}

    print(to_json(result))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()


    # display mean travel time
    mean = df['Trip Duration'].mean()

    result = {'total': total,
              'mean': mean}

    print(to_json(result))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    fmt = lambda s: ' | '.join(['{} ({})'.format(i, s[i]) for i in s.index])
    fmt2 = lambda d: ' | '.join(['{} ({})'.format(k, d[k]) for k in d.keys()])
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = fmt(df.groupby(['User Type'])['User Type'].count())

    # Display counts of gender
    if 'Gender' in df:
        gender = fmt(df.groupby(['Gender'])['Gender'].count())
    else:
        gender = 'N/D'

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
    else:
        earliest = 'N/D'
        most_recent = 'N/D'
        most_common = 'N/D'
        

    result = {'user types': user_types,
              'gender': gender,
              'year of birth': fmt2({'earliest': earliest,
                                'most recent': most_recent,
                                'most common': most_common})}

    print(to_json(result))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def top_raw_data(df, n):
    i = 0

    rows = df.shape[0]

    while True:
        question = input('\nWould you like to see then next {} lines of raw data? Enter "q" to quit: '.format(n))
        if question.lower() == 'q':
            break

        paged_df = df.iloc[i : i+n]

        if paged_df.size != 0:
            print(paged_df)
        
        rows -= paged_df.shape[0]

        if rows <= 0:
            print('\n' + '-'*40)
            print('You have hit the end of the file.')
            print('-'*40)
            break

        i += n

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        top_raw_data(df, 5)

        restart = input('\nWould you like to restart? Enter "yes" or "no": ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
