import csv
import ast
from configure import *
from collections import defaultdict
import pandas as pd


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

def get_most_common_characters(path, num_of_characters=MAX_CHARACTERS):
    with open(path, newline='') as f:
        df = pd.read_csv(f)
        scenes = df['Characters']

        characters_counter = defaultdict(int)
        for scene in scenes:
            for character in ast.literal_eval(scene):
                characters_counter[character] += 1

        my_dict = {k: v for k, v in sorted(characters_counter.items(), key=lambda item: item[1], reverse=True)}
        most_common = list(my_dict.keys())[:num_of_characters]
        print(most_common)
        return most_common


def clean_labels(path):
    new_data = []
    most_common_characters = get_most_common_characters(path)
    with open(path, newline='') as f:
        data = csv.reader(f)
        
        for i, line in enumerate(data):

            if i ==0: continue
            cleaned_characters = []
            for character in ast.literal_eval(line[CHARACTERS]):
                if character in most_common_characters:
                    cleaned_characters.append(character)
            if cleaned_characters:
                new_line = line[:CHARACTERS] + [cleaned_characters]
                new_data.append(new_line)

# TODO remove lines with irrelevant speakers (not in top 30)
    new_path = 'part2_data_cleaned_characters.csv'
    with open(new_path, 'w+', newline='') as f:
        w = csv.writer(f)
        w.writerows(new_data)

clean_labels('Part_2/part2_data_cleaned.csv')


# clean_lines_with_scenes(part2_data_path)


