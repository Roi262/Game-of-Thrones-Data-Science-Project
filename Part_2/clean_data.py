import csv
import ast
from configure import *


def clean_lines_with_scenes(path):
    with open(path, newline='') as f:
        data = csv.reader(f)
        cleaned_data = []
        data_len = 0
        for i, line in enumerate(data):
            if i == 0: continue
            speaker = line[SPEAKER]
            # override exceptions
            if speaker in EXCEPTIONS.keys():
                speaker = EXCEPTIONS[speaker]

            characters = ast.literal_eval(line[CHARACTERS])
            for character in characters:
                if speaker.lower() in character.lower():
                    line[SPEAKER] = character
                    cleaned_data.append(line)
                    break
                # print(speaker, ': ', characters)
            data_len = i
    
    new_path = 'part2_data_cleaned.csv'
    with open(new_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerows(cleaned_data)

    # record number of lines lost in this process
    print(data_len - len(cleaned_data))

            # otherwise, change name of speaker to his formal name
            # Exceptions: ned-Eddard stark; littlefinger-Petyr Baelish, ser dontos- dontos, dolorous edd - eddison Tollet, marwyn-Archmaester Ebrose,dany - Daenerys Targaryen
            # clean ', i.e. Mole's town whore
            # to check more, print line in every instance of 1

clean_lines_with_scenes(part2_data_path)
