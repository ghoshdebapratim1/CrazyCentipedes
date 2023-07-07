#import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
#import seaborn as sns
import matplotlib.pyplot as plt
import io
import numpy as np 
#import matplotlib.pyplot as plt
#import numpy as np
#import plotly.figure_factory as ff

#look for more information here https://docs.streamlit.io/library/cheatsheet
df = pd.read_csv('mxmh_survey_results.csv')

#Title
st.title("Music and Mental Health")



## Section 0
st.header('Introduction')
st.write('A data analysis on a study that compares the effects between certain music genres and mental health. The following information was derived from an extensive survey with over 700 participants, asking them about things such as their favorite music genres and how often they listen to music, as well as their self-reported effects on mental health, such as anxiety, OCD, insomnia, and depression. In this analysis, we further explored that relationship by creating connections between several different elements of the survey.')

st.write("Team Members: ")
st.markdown("- Devika Kurup ")
st.markdown("- Yeojoon Hur ")



st.header('Data Description ')
st.write('We got our data from the "Music and Mental Health Survey" done by Cathering Rasgaitis on Kaggle. This dataset consists of 736 rows and 33 columns.')

st.write(df.head())
# st.subheader('Data Science Workflow')
# st.write('Step 1: Research and capture the data')
# st.write('Step 2: Inspect and clean the data')
# st.write('Step 3: Formulate hypothesis')
# st.write('Step 4: Analyze the data through data visualizations')
# st.write('Step 5: Answer the hypothesis using the visualizations')
# st.write('Step 6: Communicate the results to others')

#Section 1 - Data Inspection and Cleaning
st.header('Section 1 - Data Pre Processing ')

st.write("Before the visualization of our data, we removed columns that were irrelevant to our hypothesis by utilizing the drop() function. We then checked if there were other null values present in the data using the Isnull ().sum() function, which enabled easy identification of columns with corresponding missing values. Implementing the mode and mean functions allowed for quick replacement of the missing values per column. However, unlike the other columns that were of the data type: object,  the ‘BPM’ column was the only column with the data type: float. Thus, we used the isnull() function to create another data frame with the missing values of the ‘BPM’ column. After that, we created a list of genres with the missing values, and filled the missing values of each genre by looping through the list and filling it with a mean value of each genre.")
# Yeojoon talk about removing irrelevant and how you replaced  missing values 
## Dropping unnecessary columns
df = df.drop(["Timestamp","Permissions"], axis=1)

## Replace Missing Values 

df['Primary streaming service']=df['Primary streaming service'].fillna(df['Primary streaming service'].mode()[0])
df['Age']=df['Age'].fillna(df['Age'].mean())## Replace Missing Values
df['While working']=df['While working'].fillna(df['While working'].mode()[0])
df['Instrumentalist']=df['Instrumentalist'].fillna(df['Instrumentalist'].mode()[0])
df['Composer']=df['Composer'].fillna(df['Composer'].mode()[0])
df['Foreign languages']=df['Foreign languages'].fillna(df['Foreign languages'].mode()[0])
df['Music effects']=df['Music effects'].fillna(df['Music effects'].mode()[0])
miss_bpm=df[df['BPM'].isnull()==True]
miss_bpm_genre= list(miss_bpm['Fav genre'].unique())
for i in miss_bpm_genre:
  df['BPM']=df['BPM'].fillna( round(df[df['Fav genre']==i]['BPM'].mean(),0) )




## Section 2 - Data Visualisation 

st.header('Section 2 - Hypothesis or Questions to be answered from the data  ')

#Favorite Genre of Music - Pie chart - 1st Chart
st.subheader('Question 1 : What is People\'s Favorite Genre of Music? ')
popular_genre = px.pie(df, names = 'Fav genre', title = 'Favorite Genre of Music')
popular_genre.update_traces(pull=[0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
st.plotly_chart(popular_genre)
st.write('Before we got too far into our analysis, we wanted to get some background information about the survey and it\'s participants. We explored what the respondent\'s favorite genre is, and, as demonstrated by the graph, rock is the genre that most of the participants said was their favorite.')

#Hours Per Day - Histogram - 2nd Chart
st.subheader('Question 2 : How Long Do Most People Listen to Music Per Day? ')
import math
bin_width= 2
nbins = math.ceil((df['Hours per day'].max() - df['Hours per day'].min()) / bin_width)
hours_per_day = px.histogram(df, x='Hours per day', title = 'How Long People Listen to Music')
hours_per_day.update_traces(xbins=dict(
        start=0.0,
        end=24.0,
        size=2
    ))
st.plotly_chart(hours_per_day)
st.write('We also wanted to see how long the respondents listened to music for on any given day. As we can see from the graph, 299 people said they listen to music for anywhere from 2-4 hours a day, making them the majority.')

#Hours of those who listen while working versus those who don't - Bar graph - 3rd Chart 
st.subheader('Question 3 : Do Those Who Listen to Music While Working Listen For More Hours A Day Than Those Who Don\'t? ')
df_plot = pd.DataFrame(df.groupby(['While working'])['Hours per day'].mean().reset_index())
fig = px.bar(df_plot, x = 'While working', y = 'Hours per day', title = "Hours Per Day of Those Who Listen While Working Versus Those Who Don't")
st.plotly_chart(fig)
st.write('The last piece of background information we wanted to look at was whether or not people who listened to music while working spent more time listening to music than those who didn\'t. The graph shows that on average, the people who listened to music while working listened for about two hours more than those who don\'t.')
#Music and Depression - Sunburst chart - 5th Chart
st.subheader('Question 4 : Which Music Genre Best Helps With Depression?')
df["Depression"]=df["Depression"].apply(str)
df_combinations=(df.groupby(["Depression","Music effects","Fav genre"])
                            .size()
                            .reset_index()
                            .rename(columns={0:"count"}))
fig = px.sunburst(df,
                  path=["Depression","Music effects","Fav genre"],
                  title="Music and Depression",
                  color="Depression",
                  height = 1000,
                  width = 1000)
st.plotly_chart(fig)
st.write('Now we start comparing the effects of music and mental health. We wanted to explore which music genre, if any, best helped to alleviate depression. This graph is read from the inside to the outside. The innermost circle contains the level of depression that the respondents self-reported. From any given section of the innermost circle, if you move directly outwards to the next section, you will see the respondent\'s self-reported effects of the music on their mental health. Moving outwards from there, you see which genre of music the majority of people in those categories prefer listening to, indicating that that genre is responsible for those effects on their mental health. For example, this graph shows us that, generally, rock, pop, and metal worked best to improve people\'s mental health.')

#Music and Anxiety - Heatmap - 6th Chart
st.subheader('Question 5 : Which Music Genre Best Helps With Anxiety? ')
df['Combo1'] = df['Music effects']+'-'+df['Anxiety'].apply(str)
revised = pd.crosstab(df['Fav genre'], df['Combo1'])
music_anxiety = px.imshow(revised, height = 800, width = 1000, title = 'Music and Anxiety')
st.plotly_chart(music_anxiety)
st.write('Next, we explored the correlations between music and levels of anxiety in the form of a heatmap. The X-axis (the horizontal axis) has combinations of both the music effects and levels of anxiety, while the Y-axis (the vertical axis), has the different favorite genres of music. The intensity of colors on the map represents the amount of people that have submitted any given response. The darker the color, the higher the count of people that submitted those answers. The graph shows that rock music best improves people\'s anxiety, despite them having high levels of it, as shown by the darkest colors around that area.') 

#Music and Insomnia - Bar graph - 7th Chart
st.subheader('Question 6 : Which Music Genre Best Helps With Insomnia?')
df_plot=(df.groupby(['Fav genre'])['Insomnia'].mean().reset_index())
df_plot=df_plot.sort_values(["Insomnia"],ascending=True)

fig = px.bar(df_plot, x="Fav genre", y="Insomnia", title = 'Music and Insomnia')
st.plotly_chart(fig)

st.write('The chart above explores the relationship between types of music and self-perceived levels of insomnia.On average, those who like listening to rap seem to have the lowest levels of insomnia, while those who like listening to LoFi seem to have the highest levels of insomnia.')

#Music and OCD - Box plot - 8th Chart
st.subheader('Question 7 : Which Music Genre Best Helps With OCD?')
music_OCD = px.box(df, x = 'Fav genre', y = 'OCD', title = 'Music and OCD')
st.plotly_chart(music_OCD)
st.write('The last relationship we explored was the relationship between music and levels of OCD. The blue bar inside the boxes represent the median levels of OCD for any given music genre. The bottom line of the box represents the 25th percentile, while the top line represents the 75th percentile. The bigger the box, the higher the amount of variance between all the individuals that prefer that type of music. People that listen to folk and latin music generally have lower amounts of OCD, as they have low medians and lower variances (as shown by the more compact boxes).')

st.header("Conclusion")

