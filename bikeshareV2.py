import time
import pandas as pd
import numpy as np
from decimal import Decimal

CITYDATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# establish valid input values
CITY_LIST = CITYDATA.keys()
MONTH_LIST = ['january','february','march','april','may','june','july','august','september','october','november','december','all']
DAY_LIST = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

#Set debug on/off
debug = 0

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    if debug == 0:
        # get user input for city (chicago, new york city, washington).
        # For each input, use a while loop to handle invalid inputs
        loop = 0    
        while loop == 0:
            city = input("Enter the city (chicago, new york city, washington): ").lower()
            if city in CITY_LIST:
                loop = 1
    
        # get user input for month (all, january, february, ... , june)
        loop = 0
        while loop == 0:
            month = input("Enter the month (all, january, february, ... , june): ").lower()
            if month in MONTH_LIST:
                loop = 1
    
        # get user input for day of week (all, monday, tuesday, ... sunday)
        loop = 0
        while loop == 0:
            day = input("Enter the day of week (all, monday, tuesday, ... sunday): ").lower()
            if day in DAY_LIST:
                loop = 1
    else:   
        #quick view defaults:
        """
        city  = 'chicago'
        month = 'all'
        day   = 'friday'
        """
        city  = 'new york city'
        month = 'july'
        day   = 'wednesday'
        print('\nDEBUG MODE\n')

    print('-'*40)
    print("\nRunning with the following parameters: \nCity: '{}', Month: '{}', Day: '{}'".format(city,month,day))
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
    #capitalize the user's inputs to match the input file
    day = day.capitalize()
    month = month.capitalize()
    
    df = pd.read_csv(CITYDATA[city])
    
    #show data for debug purposes:
    if debug == 1:
        print(df.head())

    #reformat existing columns
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    
    #Add new calculated columns
    df["Month"] = df["Start Time"].dt.strftime("%B")
    df["Day"] = df["Start Time"].dt.strftime("%A")
    df["Hour"] = df["Start Time"].dt.strftime("%H")

    #Apply month filter if required:    
    if month != "All":
        df = df[df.Month == month]

    #Apply day filter if required: 
    if day != "All":
        df = df[df.Day == day]

    #show data for debug purposes:
    if debug == 1:
        print(df.head())
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    reportStr = "Most common month: {}, # of times: {}"
    reportVal  = df['Month'].value_counts().max()
    reportOn = df['Month'].value_counts().idxmax()
    print(reportStr.format(reportOn, reportVal))

    # display the most common day of week
    reportStr = "Most common day of week: {}, # of times: {}"
    reportVal  = df['Day'].value_counts().max()
    reportOn = df['Day'].value_counts().idxmax()
    print(reportStr.format(reportOn, reportVal))

    # display the most common start hour
    reportStr = "Most common start hour: {}, # of times: {}"
    reportVal  = df['Hour'].value_counts().max()
    reportOn = df['Hour'].value_counts().idxmax()
    print(reportStr.format(reportOn, reportVal))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    reportStr = "Most common start station: {}, # of times: {}"
    reportVal  = df['Start Station'].value_counts().max()
    reportOn = df['Start Station'].value_counts().idxmax()
    print(reportStr.format(reportOn, reportVal))
    
    # display most commonly used end station
    reportStr = "Most common end station: {}, # of times: {}"
    reportVal  = df['End Station'].value_counts().max()
    reportOn = df['End Station'].value_counts().idxmax()
    print(reportStr.format(reportOn, reportVal))

    # display most frequent combination of start station and end station trip
    ctDf = pd.DataFrame("Start: " + df['Start Station'] + " --> End: " + df['End Station'], columns=["Trip"])
    reportStr = "Most common trip stations: {}, # of times: {}"
    reportVal  = ctDf['Trip'].value_counts().max()
    reportOn = ctDf['Trip'].value_counts().idxmax()
    print(reportStr.format(reportOn, reportVal))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    reportStr = "Total travel time: {}"
    reportVal  = df['Trip Duration'].sum()
    #print(reportStr.format(round(Decimal(reportVal),2)))
    print(reportStr.format(reportVal))

    # display mean travel time
    reportStr = "Mean travel time: {}"
    reportVal  = df['Trip Duration'].mean()
    #print(reportStr.format(round(Decimal(reportVal),2)))
    print(reportStr.format(reportVal))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of each type of user:")
    print(df.groupby(['User Type']).size())
    print("\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nCount of each gender:")
        print(df.groupby(['Gender']).size())
    else:
        print("Gender information is not available for this city.\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        reportStr = "\nBirth Year: Earliest: {}, Most Recent: {}, Most Common: {}"
        rptEarly  = int(df['Birth Year'].min())
        rptRecent = int(df['Birth Year'].max())
        rptCommon = int(df['Birth Year'].value_counts().idxmax())
        print(reportStr.format(rptEarly, rptRecent, rptCommon))
    else:
        print("Birth Year information is not available for this city.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Display raw data 5 rows at a time if the user would like to see it"""
    #initialize the variable to display data
    startIdx = 0
    validAnswers = ['y', 'n']

    loop = 0    
    while loop == 0:
        display = input('\nWould you like to see 5 rows of raw data? (y/n):').lower()
        if display in validAnswers:
            loop = 1

    while display == 'y':
        #display it
        print(df[startIdx:startIdx+5].values)

        #increment start row
        startIdx += 6
    
        #ask again
        loop = 0    
        while loop == 0:
            display = input('See 5 more rows? (y/n):').lower()
            if display in validAnswers:
                loop = 1

def main():

    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #print(df.empty)

        if df.empty:
            print("\nThere is no data for this combination of parameters!  Resetting...")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
