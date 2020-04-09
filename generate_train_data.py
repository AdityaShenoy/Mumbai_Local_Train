# This script assumes that time gap between 2 stations would always remain same

import pandas as pd

# These are the routes from end station to end station
end_to_end_routes = [
  ['CSMT', 'MASJID', 'SANDHURST ROAD', 'BYCULLA', 'CHINCHPOKLI', 'CURREY ROAD',
  'PAREL', 'DADAR', 'MATUNGA', 'SION', 'KURLA', 'VIDYAVIHAR', 'GHATKOPAR',
  'VIKHROLI', 'KANJUR MARG', 'BHANDUP', 'NAHUR', 'MULUND', 'THANE', 'KALVA',
  'MUMBRA', 'DIVA JN', 'KOPAR', 'DOMBIVLI', 'THAKURLI', 'KALYAN', 'SHAHAD',
  'AMBIVLI', 'TITWALA', 'KHADAVLI', 'VASIND', 'ASANGAON', 'ATGAON', 'THANSIT',
  'KHARDI', 'UMBERMALI', 'KASARA'],
  ['CSMT', 'MASJID', 'SANDHURST ROAD', 'BYCULLA', 'CHINCHPOKLI', 'CURREY ROAD',
  'PAREL', 'DADAR', 'MATUNGA', 'SION', 'KURLA', 'VIDYAVIHAR', 'GHATKOPAR',
  'VIKHROLI', 'KANJUR MARG', 'BHANDUP', 'NAHUR', 'MULUND', 'THANE', 'KALVA',
  'MUMBRA', 'DIVA JN', 'KOPAR', 'DOMBIVLI', 'THAKURLI', 'KALYAN', 'VITHALWADI',
  'ULHAS NAGAR', 'AMBERNATH', 'BADLAPUR', 'VANGANI', 'SHELU', 'NERAL',
  'BHIVPURI ROAD', 'KARJAT', 'PALASDHARI', 'KELAVLI', 'DOLAVLI', 'LOWJEE',
  'KHOPOLI']
]

# Time between stations
time_between_stations = [
  [3, 2, 3, 2, 2, 3, 3, 3, 3, 4, 3, 3, 4, 3, 3, 3, 3, 5, 4, 6, 4, 5, 3, 4, 7, 4,
  3, 6, 7, 7, 9, 9, 4, 6, 5, 13],
  [3, 2, 3, 2, 2, 3, 3, 3, 3, 4, 3, 3, 4, 3, 3, 3, 3, 5, 4, 6, 4, 5, 3, 4, 7, 4,
  3, 4, 7, 9, 4, 4, 7, 9, 5, 7, 3, 4, 6]
]

# Initialize an empty dictionary of routes from all station to all station
routes = dict()

# Initialize an empty dictionary of time delays between adjacent stations
time_delay = dict()

# For all end to end routes
for a, e2e_route in enumerate(end_to_end_routes):

  # For all start stations
  for i, start in enumerate(e2e_route):

    # For all end stations
    for j, end in enumerate(e2e_route):

      # If they are not equal
      if start != end:

        # Store the list index and sub list indices of both direction
        routes[start, end] = a, i, j
        routes[end, start] = a, j, i

        # Store the time delay if the stations are adjacent
        if abs(i - j) == 1:
          time_delay[frozenset([start,end])] = time_between_stations[a][min(i,j)]

# Open the train_data file
with open('train_data.csv', 'w') as out:

  # Write header in output
  out.write('start,end,start_time,speed,station,time,time_of_day\n')

  # Open the input file
  with open('input_for_generate_train_data.txt') as inp:

    # For all lines in the file
    for line in inp.readlines():

      # Extract start, end and time from line
      start, end, time = line.strip().split(',')
      start, end = start.upper(), end.upper()

      # Extract route info
      a, i, j = routes[start, end]

      # Direction for up or down
      direction = (j-i)//abs(j-i)

      # Find min and max of i and j
      mx, mn = max(i, j), min(i, j)

      # Find route from the route info
      route = end_to_end_routes[a][mn: mx+1][::direction]

      # Format the time
      start_time = f'{time[:2]}:{time[2:]}'

      # Time of day for temporal ordering of stations in journey
      time_of_day = int(time[:2])*60 + int(time[2:])

      # Train identifier
      train_id = f'{start},{end},{start_time},S'

      # Write info for first station
      out.write(f'{train_id},{start},{start_time},{time_of_day}\n')

      # Extract hour and minute from time
      hour, minute = int(time[:2]), int(time[2:])

      # Store the previous station
      prev_station = start

      # For all stations except for first
      for station in route[1:]:

        # Add minute delay to minute and time of day
        minute += time_delay[frozenset([station, prev_station])]
        time_of_day += time_delay[frozenset([station, prev_station])]

        # Current station becomes previous_station for next station
        prev_station = station

        # If minute is an hour or more
        if minute > 59:

          # Calculate hour and minute
          minute %= 60
          hour = (hour + 1) % 24
        
        # Write output
        out.write(f'{train_id},{station},{hour:02}:{minute:02},{time_of_day}\n')