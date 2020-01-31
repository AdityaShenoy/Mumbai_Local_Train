from pandas import DataFrame

# List containing station names between extreme ends that covers all other paths
end_to_end = [
  'CSMT,MASJID,SANDHURST ROAD,BYCULLA,CHINCHPOKLI,CURREY ROAD,PAREL,DADAR,MATUNGA,SION,KURLA,VIDYAVIHAR,GHATKOPAR,VIKHROLI,KANJUR MARG,BHANDUP,NAHUR,MULUND,THANE,KALVA,MUMBRA,DIVA JN,KOPAR,DOMBIVLI,THAKURLI,KALYAN,SHAHAD,AMBIVLI,TITWALA,KHADAVLI,VASIND,ASANGAON,ATGAON,KHARDI,KASARA',
  
  'CSMT,MASJID,SANDHURST ROAD,BYCULLA,CHINCHPOKLI,CURREY ROAD,PAREL,DADAR,MATUNGA,SION,KURLA,VIDYAVIHAR,GHATKOPAR,VIKHROLI,KANJUR MARG,BHANDUP,NAHUR,MULUND,THANE,KALVA,MUMBRA,DIVA JN,KOPAR,DOMBIVLI,THAKURLI,KALYAN,VITHALWADI,ULHAS NAGAR,AMBERNATH,BADLAPUR,VANGANI,SHELU,NERAL,BHIVPURI ROAD,KARJAT,PALASDHARI,KELAVLI,DOLAVLI,LOWJEE,KHOPOLI'
]

# Initialize empty dictionary of paths
paths = {}

# For all end to end paths
for e in end_to_end:

  # Split the stations on comma
  stations = e.split(',')

  # For all source stations
  for i, station1 in enumerate(stations):

    # For all destination stations
    for j, station2 in enumerate(stations):

      # If source and destination are same, skip this iteration
      if station1 == station2:
        continue

      # If this path has already been covered in previous iterations, skip this iteration
      if f'{station1}-{station2}' in paths:
        continue

      paths[f'{station1}-{station2}'] = ','.join(stations[i:j+1])

# Initialize data as a dictionary containing empty columns
data = {'Source': [], 'Destination': [], 'Start Time': [], 'Speed': [], 'Station': [], 'Time': [], 'Platform': []}

# Loop until user enters yes on prompt
while input('Do you want to add more trains?(y/n) ') in 'yY':

  # Take inputs from user
  source = input('Enter source: ').upper()
  destination = input('Enter destination: ').upper()
  speed = input('Enter speed:(S/F) ').upper()
  start_time = 0

  # Iterate through all stations in the path between source and destination
  for station in paths[f'{source}-{destination}'].split(','):

    print(f'Enter data for {station}')

    # Take inputs from user
    if speed == 'F':
      if input('Does this train halt here?(y/n) ') in 'nN':
        continue
    
    h, m = input('\tEnter time:(h[h] m[m]) ').split()
    time = f'{h:>02}:{m:>02}'
    platform = input('\tEnter platform:(pf1[-pf2]) ')

    # Record the first time input for source
    if station == source:
      start_time = time
    
    # Record the inputs in the data dictionary
    data['Source'].append(source)
    data['Destination'].append(destination)
    data['Start Time'].append(start_time)
    data['Speed'].append(speed)
    data['Station'].append(station)
    data['Time'].append(time)
    data['Platform'].append(platform)

# Write the new/updated data to train_data.csv
DataFrame(data).to_csv('train_data.csv', index=False)