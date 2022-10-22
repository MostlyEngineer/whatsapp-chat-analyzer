from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


extractor= URLExtract()

def fetch_stats(selected_user,df):

###### restructured code
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    # number of messages
    num_messages = df.shape[0]

    # number of wors
    words=[]
    for msg in df['message']:
        words.extend(msg.split())

    # fetch number of media message
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # link shared
    links=[]
    for msg in df['message']:
        links.extend (extractor.find_urls(msg))
    return num_messages, len(words), num_media_msg, len(links)

# most active use
def most_active_users(df):
    x = df['user'].value_counts().head()
    new_df1 = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'Percentage'})
    return x, new_df1

# word cloud
def create_wordcloud(selected_user,df):


    f=  open('stopwords_hinglish.txt','r')
    stop_words = f.read()
    print(stop_words)


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    temp = df[df['user'] != 'group_notification']
    temp =temp[temp['message'] != '<Media omitted>\n']

    # stopwords removal
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)


    wc =WordCloud(width=500, height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc

#most common words

def most_common_words(selected_user,df):

    f=  open('stopwords_hinglish.txt','r')
    stop_words = f.read()
    print(stop_words)


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    temp = df[df['user'] != 'group_notification']
    temp =temp[temp['message'] != '<Media omitted>\n']

    words=[]

    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
        words.extend(msg.split())
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

# emoji helper

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis=[]
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] +'-'+ str(timeline['year'][i]))

    timeline['time']=time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline= df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap





    