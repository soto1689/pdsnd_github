import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def city_filter_method(city):
    while city == "none":
        city = input("\nEnter what city you would like to analyze.\n\nYou are able to choose one of below three cities\n\n chicago \n new york city \n washington \n\n").lower()
        if city == "chicago"or city =="new york city"or city == "washington":
            print("\nAwesome! \U0001F603  Lets get started and analyze bikeshare data from {} \n".format(city.title()))
            break
        else:
            print("\n'{}' was not a valid entry.\n".format(city))
            city = "none"
    return city

def get_filters():
    """
    Asks user to specify a city, month, and day of week to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = "none"
    city = city_filter_method(city)
    
    
    # get user input for month (all, january, february, ... , june)
    month = "none"
    filter_month = "none"
    while filter_month == "none":
        filter_month = input("Would you also like to analyze your data by month? yes or no?\n\n").lower()
        if filter_month == "yes":
             while month == "none":
                month = input("\nEnter what month you would like to analyze.\n\nWe only have 2017 data from January - June. Please enter one of the below options\n\n january \n february \n march \n april \n may \n june \n\n").lower()
                if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                    print("\nGreat! \U0001f600  We will make sure to filter your insights based on avalible month data for {} \n".format(month))
                    break
                else:
                    print("\n'{}' was not a valid entry.\n".format(month))
                    month = "none"
        elif filter_month == "no":
            print("\nThank you for your feedback\n")
            month = "all"
            break
        elif filter_month != "yes" or filter_month != "no":
            print("\nThat was not a valid entry.\n")
            filter_month = "none"

    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = "none"
    filter_day = "none"
    while filter_day == "none":
        filter_day = input("We can also analyze your data by the day of the week. Would you like to filter by day? yes or no?\n\n").lower()
        if filter_day == "yes":
             while day == "none":
                day = input("\nEnter what day of the week you would like to analyze.\n\nPlease enter one of the below options\n\n Monday \n Tuesday \n Wednesday \n Thursday \n Friday \n Saturday \n Sunday \n\n").title()
                if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']:
                    print("\n\U0001F44D!!!!  We will make sure to filter your insights based on the day of the week and drill down on 2017 {} US bikeshare rentals in {} specifically for rentals that occurred on {}s \n".format(month,city.title(),day))
                    break
                else:
                    print("\n'{}' was not a valid entry.\n".format(day))
                    day = "none"
        elif filter_day == "no":
            print("\nThank you for your feedback\n")
            day = "all"
            break
        elif filter_day != "yes" or filter_day != "no":
            print("\nThat was not a valid entry.\n")
            filter_day = "none"
            
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() # in older version of pandas "dt.day_name()"" == "dt.weekday_name"


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']    
    common_month = df['month'].mode()[0]
    common_month_value = df['month'].value_counts()[common_month]
    print("The most popular month for bikeshare rentals with a total count of {} is:\n{}({})\n".format(common_month_value, months[common_month-1].title(), common_month,))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    common_day_value = df['day_of_week'].value_counts()[common_day]
    print("The most frequent day for bikeshare travel with a total count of {} is:\n{}\n".format(common_day_value, common_day))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_start_hr = df['start_hour'].mode()[0]
    common_start_hr_value = df['start_hour'].value_counts()[common_start_hr]
    print("The most common start hour with a total count of {} is:\n{}:00\n".format(common_start_hr_value, common_start_hr))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    pop_start_station_val = df['Start Station'].value_counts().head(1)[0]
    
    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    pop_end_station_val = df['End Station'].value_counts().head(1)[0]
    
    print("\nThe most popular start station with a count of {} is:\n{}".format(pop_start_station_val, pop_start_station))
    print("\nThe most popular end station with a count of {} is:\n{}".format(pop_end_station_val, pop_end_station))
    
    # display most frequent combination of start station and end station trip
    Start_End_Combo = df.groupby(['Start Station', 'End Station']).size().reset_index().rename(columns={0:'Count'}) # Reference 1 in Readme.txt
    print("\nThe most frequent combination of start and end station trips with a total count of {} is ...\n".format(Start_End_Combo['Count'].max()))
    print(Start_End_Combo[Start_End_Combo['Count'] == Start_End_Combo['Count'].max()])    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_min = (df['Trip Duration'].sum())/60
    print("Total Travel Duration in Minutes: {}".format(total_travel_min))
    
    # display mean travel time
    average_travel_min =(df['Trip Duration'].mean())/60
    print("Average Travel Duration in Minutes: {}".format(average_travel_min))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city,df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of User Types:\n{}".format(df['User Type'].value_counts()))
    
    # Display counts of gender
    while True:
        if city in ['new york city', 'chicago']:
            # Display earliest, most recent, and most common year of birth
            print("\nEarliest Year of Birth: {}".format(df['Birth Year'].min().astype(int)))
            print("Most Recent Year of Birth: {}".format(df['Birth Year'].max().astype(int)))
            print("Most Common Year of Birth: {}".format(df['Birth Year'].mode()[0].astype(int)))
            return print("\nCount of Gender Types:\n{}".format(df['Gender'].value_counts()))
        elif city == "washington":
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(city,month,day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city,df)
        
        df.rename(columns={'Unnamed: 0': 'Rental_Transaction_ID'},inplace=True)
        df.set_index('Rental_Transaction_ID')
        
        show_data = input('\nWould you like to view some raw data?(yes or no)')
        start_index = 0
        end_index=6
        while show_data == 'yes':
            print(df[start_index:end_index])
            start_index = end_index
            end_index +=5
            show_data = input('\nWould you like to view more raw data?(yes or no)')
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

