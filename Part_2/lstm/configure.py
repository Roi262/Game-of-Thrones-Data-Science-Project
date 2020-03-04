import csv

# ori computer
# part2_data_path = '../Part_2/part2_data_lines_with_scenes.csv'
# CLEAN_DATA_PATH = '../Part_2/part2_data_cleaned.csv'

# roi computer
part2_data_path = 'Part_2/part2_data_lines_with_scenes.csv'
CLEAN_DATA_PATH = 'Part_2/part2_data_cleaned.csv'

EXCEPTIONS = {'ned': 'Eddard Stark',
                  'littlefinger': 'Petyr Baelish', 
                  'ser dontos': 'Dontos Hollard', 
                  'dolorous edd': 'Eddison Tollett', 
                  'marwyn': 'Archmaester Ebrose',
                  'dany': 'Daenerys Targaryen'}

ROW_ID, SEASON, EPISODE, SCENE, LINE_IN_EP_ID, SPEAKER, LINE, CHARACTERS = (i for i in range(8))
MAX_CHARACTERS = 30


ALL_CHARACTERS_FORMAL = set()
with open(CLEAN_DATA_PATH) as f:
    data = csv.reader(f)
    for row in data:
        ALL_CHARACTERS_FORMAL.add(row[SPEAKER])

CHARACTERS_DIC = {}
for i, char in enumerate(ALL_CHARACTERS_FORMAL):
    CHARACTERS_DIC[char] = i

