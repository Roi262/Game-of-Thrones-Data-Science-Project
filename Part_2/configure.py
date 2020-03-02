

part2_data_path = '/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project - New/Part_2/part2_data_lines_with_scenes.csv'
CLEAN_DATA_PATH = 'Part_2/part2_data_cleaned.csv'
# Exceptions: ned-Eddard stark; littlefinger-Petyr Baelish,dany - Daenerys Targaryen
EXCEPTIONS = {'ned': 'Eddard Stark',
                  'littlefinger': 'Petyr Baelish', 
                  'ser dontos': 'Dontos Hollard', 
                  'dolorous edd': 'Eddison Tollett', 
                  'marwyn': 'Archmaester Ebrose',
                  'dany': 'Daenerys Targaryen'}

ROW_ID, SEASON, EPISODE, SCENE, LINE_IN_EP_ID, SPEAKER, LINE, CHARACTERS = (i for i in range(8))


