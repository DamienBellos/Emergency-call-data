# Example data analysis in Pandas
# Data from Kaggle https://www.kaggle.com/mchirico/montcoalert

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
df = pd.read_csv('911.csv')

# To display the top 5 Zipcodes and Townships for 911 calls
print('Zipcodes', df['zip'].value_counts().head(5), sep='\n')
print('\n')
print('Township', df['twp'].value_counts().head(5), sep='\n')
print('\n')

# Create a new column "Reason" then display the categorical reason for the call
df['Reason'] = df['title'].apply(lambda x: x.split(':')[0])
print('Grouped reason for call:', df['Reason'].value_counts(), sep='\n')

# Displays countplot of calls by reason
sns.countplot(df['Reason'], palette='deep')
plt.title('Reason for 911 call ')
plt.show()

# Convert timeStamp to data time object and create separate columns for hour, month and day
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

time = df['timeStamp'].iloc[0]
df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day'] = df['timeStamp'].apply(lambda time: time.dayofweek)

# Maps the numbers to the corresponding day of the week
dmap = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
df['Day'] = df['Day'].map(dmap)

# Displays a countplot of the calls/reason/day of the week
sns.countplot(x=df['Day'], data=df, hue=df['Reason'], palette='tab20')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Reason for 911 calls during the week')
plt.show()

# Displays a countplot of the calls/reason/month of the year
sns.countplot(x=df['Month'], data=df, hue=df['Reason'], )
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Reason for 911 calls during the month')
plt.show()

# Since months 9-11 are missing, plot the data by calls/ month
byMonth = df.groupby(by='Month').count()
byMonth['e'].plot()
plt.title('Calls per month')
plt.show()

# Create a new column with the date to plot call volume for each date
df['Date'] = df['timeStamp'].apply(lambda time: time.date())
df.groupby(by='Date')['e'].count().plot()
plt.tight_layout()
plt.title('Call volume')
plt.ylabel('Calls')
plt.show()

# Calls placed about traffic for each date
df[df['Reason'] == 'Traffic'].groupby(by='Date')['e'].count().plot()
plt.title('Traffic')
plt.ylabel('Calls')
plt.show()

# Calls placed about fire for each date
df[df['Reason'] == 'Fire'].groupby(by='Date')['e'].count().plot()
plt.title('Fire')
plt.ylabel('Calls')
plt.tight_layout()
plt.show()

# Calls placed about fire for each date
df[df['Reason'] == 'EMS'].groupby(by='Date')['e'].count().plot()
plt.title('EMS')
plt.ylabel('Calls')
plt.tight_layout()
plt.show()

# Display a heatmap and cluster map of calls over each hour for each day of the week
dayHour = df.groupby(by=['Day', 'Hour']).count()['e'].unstack()
sns.heatmap(dayHour)
plt.title('Hourly 911 call volume per day')
plt.show()

# Display a heatmap and cluster map of calls over each day for each month of the week
dayMonth = df.groupby(by=['Day', 'Month']).count()['e'].unstack()
sns.heatmap(dayMonth)
plt.title('Hourly 911 call volume per month')
sns.clustermap(dayMonth)
plt.title('Hourly 911 call volume per month')
plt.show()
