import pandas as pd
import numpy as np
import time

# Source and destination
src = input('Please enter a source station: ')
dest = input('Please enter a destination: ')
# src, dest = 'MATUNGA', 'NAHUR'
# src, dest = 'KARJAT', 'KASARA'

# Read the train time table data
df = pd.read_csv('train_data.csv')

# Filter the train data containing src or destination in the station column
mask = (df['station'] == src) | (df['station'] == dest)
df = df[mask]

# Get all possible trains of above filtered data
trains = df.drop_duplicates(subset='train_id')

# Initialize 2 empty dataframes
final_trains = pd.DataFrame()

# Iterate for all trains
for i in range(len(trains)):

  # ith train data
  train = trains.iloc[i]

  # Filter for train id
  mask1 = df['train_id'] == train['train_id']
  df1 = df[mask1]

  # If the train passes only one of src or dest, continue
  if len(df1) == 1:
    continue

  # Separate src and destination row
  src_row = df1[df1['station'] == src].iloc[0]
  dest_row = df1[df1['station'] == dest].iloc[0]

  # If train is going in the correct direction
  if src_row['time_of_day'] < dest_row['time_of_day']:

    # Append the train to final train
    final_trains = final_trains.append(df1)

# If there are no direct trains from src to dest
if len(final_trains) == 0:

  # Tell user that no direct trains are available
  print('There are no direct trains available between these stations.')
  print('Please try inputting intermediate stations')

else:

  # Predictions
  final_trains['predicted_time'] = final_trains['time_of_day'] + \
                              np.random.randint(4, size=len(final_trains)) * 60
  final_trains['predicted_hour'] = final_trains['predicted_time'] // 3600
  final_trains['predicted_minute'] = (final_trains['predicted_time'] % \
                                      3600) // 60
  final_trains['predicted_time_str'] = final_trains['predicted_hour'].apply(
                                        lambda x: f'{x:02}'
                                       ) + ':' + \
                                       final_trains['predicted_minute'].apply(
                                        lambda x: f'{x:02}'
                                       )
  for i in range(1, 13):
    final_trains[f'predicted_crowd{i}'] = np.random.randint(
                                        10, 100, size=len(final_trains)
                                      )

  # Output the trains to output csv file
  final_trains.to_csv('output.csv', index=False)