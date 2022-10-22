import re
import pandas as pd

def preproecess(data):
    pattern = '\d+/\d+/\d+,\s\d+:\d+\s\w+\s-\s'

    messages=re.split(pattern,data)[1:]

    dates= re.findall(pattern,data)

    df = pd.DataFrame({'user_messages' :messages,'message_date': dates})
    df['message_date'] = pd.to_datetime(df[ 'message_date'], format='%m/%d/%y, %H:%M %p - ')
    df.rename(columns={'message_date': 'date'} , inplace=True)

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:# user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
            
    df['user']= users
    df['message']= messages

    df.drop(columns=['user_messages'],inplace=True)

    df['year']=df['date'].dt.year
    df['only_date']=df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['day_name']=df['date'].dt.day_name()
    df['minute']=df['date'].dt.minute

    period=[]

    for hour in df[['day_name','hour']]['hour']:
        if hour == 12:
            period.append(str(hour) + '-' + str(1))
        elif hour == 1:
            period.append(str(1) + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
    
    df['period']=period

    return df


