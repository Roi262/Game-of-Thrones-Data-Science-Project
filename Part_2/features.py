from configure import *
import ast
import csv


RELEVANT_CHARACTERS = CHARACTERS_DIC

def create_special_features():
    spoken_to_in_sent = [0] * len(RELEVANT_CHARACTERS)

    for row in data:
        line = row[LINE]
        # characters = ast.literal_eval(row[CHARACTERS])

        # 1. check whether a characters name is said in the line itself
        for character in RELEVANT_CHARACTERS:
            if character in line.split():
                # TODO add 1 in 'character spoken to' index. note that for every rele
                # we have this one hot per character code somewhere



def create_features():
    # TODO use tokenize/onehot
    create_special_features()