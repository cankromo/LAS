import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')
c = conn.cursor()

def get_time_frame() -> pd.DataFrame:
    """
    Get the time frame as a dataframe object. 

    Returns: pd.DataFrame: A dataframe object containing the timestamps of visitors.
    """
    
    df = pd.read_sql_query('SELECT times FROM visitors', conn)

    # Clean the data with the code below
    data = df.to_string().replace(' ', '').replace('&', ' ').replace('\n', '').split(';')[1:]
    L = []
   
    for dat in data: # a sample dat = [14:53:03 2023/05/11,14:53:04 2023/05/11], target = 14:53:03 2023/05/11

        if len(dat) > 25:
            
            if len(dat) > 41:
                dat = dat[:dat.index(']')+1]

            if len(dat) < 41 :
                dat = dat[:19]

            if len(dat) == 41:
                dat = dat.split(',')[0][1:]

        if len(dat) != 19:
            dat = dat[:19]

        L.append(dat)        
    
    timeframe = pd.DataFrame(L, columns=['timestamp']) # create a dataframe object from the list
    timeframe['timestamp'] = pd.to_datetime(timeframe['timestamp'])

    return timeframe


def get_presense_data() -> list[tuple]:
    """
    Get the presense data as a list of tuples form [(0, count), (1, count)].
    """

    c.execute('SELECT presense, COUNT(presense) FROM visitors GROUP BY presense')
    results = c.fetchall()
    
    return results


def get_per_month(df: pd.DataFrame) -> list[int]:
    """
    Get the number of visitors in each month as a dict form {key(month): number}
    """

    # Group the df by month
    grouped = df.groupby(df['timestamp'].dt.month)

    # Count the number of visitors in each month
    visitors_per_month = grouped.size()

    # add the missing months
    for month in range(1, 13):
        if month not in visitors_per_month.index:
            visitors_per_month[month] = 0
    
    # sort the dict by keys
    visitors_per_month = dict(sorted(visitors_per_month.items()))

    return list(visitors_per_month.values())


def get_weekly_user(df: pd.DataFrame) -> dict: # unused right now
    """
    Get the number of users that used the library up until that day of the week.
    """

    users_per_week = df.groupby(pd.Grouper(key='timestamp', freq='W-MON')).size()

    return users_per_week.values[-1]


def get_users_per_day(df) -> dict:
    """
    Returns the number of user per day in a week.
    """

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp')

    # Get the last week dates
    last_week_dates = df.loc[df['timestamp'] >= df['timestamp'].max() - pd.Timedelta(days=6), 'timestamp']
    day_counts = last_week_dates.dt.day_name().value_counts()

    # add the missing days
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        if day not in day_counts:
            day_counts[day] = 0

    # create a new dictionary with modified keys
    new_day_counts = {day[:2]: count for day, count in day_counts.items()}

    return new_day_counts


def get_by_hour(df) -> dict:
    """
    Take a dataframe as input and return a dictionary containing,
    the count of occurrences for each hour in the timestamp column.
    """

    df_grouped = df.groupby(df['timestamp'].dt.hour).size()

    # Add the missing hours
    for hour in range(9, 23):
        if hour not in df_grouped.index:
            df_grouped[hour] = 0 

    df_grouped = dict(sorted(df_grouped.items()))
    return df_grouped


def get_user_data(boolian: bool) -> list[tuple]:
    """
    Get general information of users that is presense if boolian
    is true, both presense and users if boolian is false.
    """

    query = "SELECT id, name, surname, age, email FROM visitors"

    if boolian:
        query = "SELECT id, name, surname, age, email, times FROM visitors WHERE presense = '1'"

    with conn:
        c.execute(query)    
        return c.fetchall()
