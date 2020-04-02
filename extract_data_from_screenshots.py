import cv2
import numpy as np
from string import ascii_lowercase as letters, digits
from operator import itemgetter
import re
from os import scandir

# Change this as per the location of files in your computer
FOLDER_PREFIX = 'F:\\github\\Mumbai_Local_Train'

# Input and template image folders
S_AM_FOLDER = f'{FOLDER_PREFIX}\\screenshots\\S\\AM'
S_PM_FOLDER = f'{FOLDER_PREFIX}\\screenshots\\S\\PM'
F_AM_FOLDER = f'{FOLDER_PREFIX}\\screenshots\\F\\AM'
F_PM_FOLDER = f'{FOLDER_PREFIX}\\screenshots\\F\\PM'
TEMPLATE_FOLDER = f'{FOLDER_PREFIX}\\templates'

# names of all stations
all_stations = ['CSMT', 'MASJID', 'SANDHURST ROAD', 'BYCULLA', 'CHINCHPOKLI',
              'CURREY ROAD', 'PAREL', 'DADAR', 'MATUNGA', 'SION', 'KURLA',
              'VIDYAVIHAR', 'GHATKOPAR', 'VIKHROLI', 'KANJUR MARG', 'BHANDUP',
              'NAHUR', 'MULUND', 'THANE', 'KALVA', 'MUMBRA', 'DIVA JN',
              'KOPAR', 'DOMBIVLI', 'THAKURLI', 'KALYAN', 'SHAHAD', 'AMBIVLI',
              'TITWALA', 'KHADAVLI', 'VASIND', 'ASANGAON', 'ATGAON', 'KHARDI',
              'KASARA', 'VITHALWADI', 'ULHAS NAGAR', 'AMBERNATH', 'BADLAPUR',
              'VANGANI', 'SHELU', 'NERAL', 'BHIVPURI ROAD', 'KARJAT',
              'PALASDHARI', 'KELAVLI', 'DOLAVLI', 'LOWJEE', 'KHOPOLI']


def convert_time(hour, time_of_day):

  # If the time of day is AM
  if time_of_day == 'AM':

    # Change 12 to 0 else leave the hour unchanged
    return {12: 0}.get(hour, hour)
  
  # Else if the time of day is PM
  else:

    # If time is PM add 12 to hour if not 12 else return 12
    return {h: h+12 for h in range(1, 12)}.get(hour, 12)


# mapping from script output words to above station names
op_to_station = {station.lower().replace(' ', ''):station
                for station in all_stations}

# Dictionary for storing template images
template_imgs = dict()

# For all alphabets, digits and platforms
for alpha in list(letters) + list(digits) + [f'p{n}' for n in range(1, 5)]:

  # There is no station having alphabet fqxz so continue
  if alpha in 'fqxz':
    continue

  # Load the template image
  small = cv2.imread(f'{TEMPLATE_FOLDER}\\{alpha}.jpg')

  # Convert the template image to grayscale
  template_imgs[alpha] = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)


# Open the output file
with open('output.csv', 'w') as f:

  # Write header to output file
  f.write('source,destination,start_time,speed,station,time,platform\n')

  # For all input folders
  for INPUT_FOLDER in [S_AM_FOLDER, S_PM_FOLDER, F_AM_FOLDER, F_PM_FOLDER]:

    # Scan the input folder
    with scandir(INPUT_FOLDER) as folder:

      # For each file in the folder
      for file in folder:

        # Read the image
        img = cv2.imread(f'{INPUT_FOLDER}\\{file.name}')

        # Convert the image to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Set for storing the tuple of (alpha, x, y)
        pos = set()

        # For alphabet and its gray scale template image
        for alpha, small_gray in template_imgs.items():

          # Match template with the original image
          res = cv2.matchTemplate(img_gray, small_gray, cv2.TM_CCOEFF_NORMED)

          # Arbitrary threshold for exactness of the match
          threshold = 0.95

          # Filter the locations of alphabets above threshold
          loc = np.where(res >= threshold)

          # For all points matched
          for pt in zip(*loc[::-1]):

            # Round the positions to nearest of tens multiple
            pos.add((alpha, pt[0] // 10 * 10, pt[1] // 10 * 10))

        # Convert the set to a list
        pos = list(pos)

        # Sort the positions by x and y
        pos.sort(key=itemgetter(1))
        pos.sort(key=itemgetter(2))

        # y stores the height where the current word is being formed
        y = -1

        # word stores the letters to form a word out of letters
        word = []

        # train_data stores all the words
        train_data = []

        # For all positions of alpha
        for i in pos:

          # If this position is lower than current height
          if i[2] != y:

            # If the current height is not yet been set to valid height
            if y != -1:

              # Append words
              train_data.append(''.join(word))

              # Reset the word list
              word = []
            
            # Set the current height to this height
            y = i[2]
          
          # Append the letter to the word list
          word.append(i[0])

        # Last word
        word = ''.join(word)

        # If the last word is not a list of platforms
        if not re.match('(p\\d{1,}){1,}', word):

          # Last letters should be station name
          train_data.append(word[4:])

          # First 4 letters must be time
          train_data.append(word[:4])

          # No platform number available
          train_data.append('p0')
          
        else:

          # Append the last word
          train_data.append(word)

        # Counter for train data
        i = 0

        # This list will contain all the data after filtering noise
        train_data_filtered = []

        # Line for filtered train data
        line = []

        # Train identifiers
        source = ''
        destination = ''
        start_time = ''
        speed = INPUT_FOLDER[-4]

        # AM or PM
        time_of_day = INPUT_FOLDER[-2:]

        # While all train data has not been read
        for data in train_data:

          # Separating the triplet (station, time, platform)
          if i == 0:

            # If it is a valid station name
            if data in op_to_station:

              # Append data to line
              line.append(op_to_station[data])

              # Set source if not already set
              if source == '':
                source = line[-1]
              
              # Set destination
              destination = line[-1]

              # Set i to time number
              i = 1
          
          elif i == 1:

            # If it is a valid time
            if re.match('\\d{4}', data):

              # Extract hour and minute from the time
              hour = data[:2]
              i_hour = int(hour)
              minute = data[2:]

              # If start time is not already been set
              if start_time == '':

                # Set the current time and start time
                cur_time = convert_time(i_hour, time_of_day)
                start_time = f'{cur_time:02}:{minute}'
              
              # If there is a change between AM and PM
              elif (i_hour == 12) and (cur_time not in [12, 0]):

                # Toggle the time of day
                time_of_day = {'AM': 'PM', 'PM': 'AM'}[time_of_day]

              # Set current time
              cur_time = convert_time(i_hour, time_of_day)

              # Append time to line
              line.append(f'{cur_time:02}:{minute}')

              # Set i to platform number
              i = 2
          
          else:

            # If it is a valid platform number
            if re.match('(p\\d{1,2}){1,}', data):

              # Format the platform numbers
              data_op = data.replace('p', '-').lstrip('-')

              # Append data to line
              line.append(f'{data_op}\n')

              # Append line with comma separation to filtered train data
              train_data_filtered.append(','.join(line))

              # Reset line list
              line = []

              # Set i to station number
              i = 0

        # Train identifier
        train_id = f'{source},{destination},{start_time},{speed}'

        # For all filtered data
        for data in train_data_filtered:
          
          # Write data in output file
          f.write(f'{train_id},{data}')