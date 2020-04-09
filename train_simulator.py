from pandas import read_csv, DataFrame
from random import random
import time as time
import numpy as np

# Maximum delay that a train can be late for
MAX_DELAY = 3

# Divide the whole sample space into total parts
parts = list(range(MAX_DELAY + 1, 0, -1))

# This list is the result of the above probability distribution
delay_list = list(range(MAX_DELAY+1))

# Sum all the parts
total = sum(parts)

# Initialize an empty probability threshold list
prob_threshold = [0]

# For all parts
for p in parts:

  # Append the cummulative threshold to the list
  prob_threshold.append(prob_threshold[-1] + p/total)

# Delete the dummy first value
del prob_threshold[0]

# This function adds random delay to the time passed
# Probability distribution [0, MAX_DELAY] in a half bell curve
def random_delay(y, mo, d, h, mi):

  # Pick a random number in [0, 1)
  r = random()

  # For all prob threshold
  for i, prob in enumerate(prob_threshold):

    # If it crosses the threshold
    if r < prob:

      # This will be the delay
      delay = delay_list[i]
      break
  
  # Return the time after adding delay
  return time.mktime(
          time.strptime(f'{y} {mo} {d} {h} {mi}', '%Y %m %d %H %M')
         ) + delay * 60


# Read train_data csv as time table tt
tt = read_csv('train_data.csv')

# Initialize a none dataframe for final output data
final_data = DataFrame()

# Year is 2020
y = 2020

# Iterate month from Jan to Apr
for mo in range(1, 5):

  # Iterate for all days in the month
  for d in range(1, {1: 31, 2: 29, 3: 31, 4: 30}[mo] + 1):

    print(f'{y} {mo} {d}')

    # Make a copy of time table
    df = tt.copy()

    # Add random delay to time table time
    df['actual_time'] = df['time'].apply(
                          lambda t: random_delay(y, mo, d, *t.split(':'))
                        )

    # Make actual time human readable
    df['actual_time_str'] = df['actual_time'].apply(
                              lambda t: time.strftime(
                                '%Y/%m/%d %H:%M', time.localtime(t)
                              )
                            )

    # Append this date's data to final data
    final_data = final_data.append(df, ignore_index=True)

# Add random crowd data to the final data
final_data['crowd'] = np.random.randint(10, 100, size=len(final_data))

# Store the final data in the csv
final_data.to_csv('train_log.csv', index=False)