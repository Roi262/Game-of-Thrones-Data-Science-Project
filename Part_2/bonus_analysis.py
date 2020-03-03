from configure import *
# 1 pairs of characters who talk to each other most


RELEVENT_CHARACTERS = ALL_CHARACTERS_FORMAL

def get_both_char_lines():
    """returns one list of all lines character A says and
     another list of all lines character B says 
    """

def score_function(rows_in_convo):
    for row in rows_in_convo:
        char1_lines, char2_lines = get_both_char_lines()


def get_conversations(char_1, char_2, conversation_thresh, noise = 2):
    """get all conversations of these 2 characters
    
    Arguments:
        char_1 {[type]} -- Character 1
        char_2 {[type]} -- Character 2
        conversation_thresh {[int]} -- minimum amount of consecutive lines between 2 
        characters for the lines to be considered a conversation
        noise {[int]} -- maximum number of rows spoken by characters other than 1 and 2 which we 
        can disregard in the conversation

    Returns:
        conversations {2D array} -- an array of arrays of rows depicting conversations
    """
    conversations = []
    for row in data:
        row_counter = 0
        conversation = []
        while row[SPEAKER] == char_1 or row[SPEAKER] == char_2:
            conversation.append((row[SPEAKER], row[LINE]))
            row_counter += 1
        if row_counter < conversation_thresh:
            continue
        conversations.append(conversation)
    return conversations


def best_friends():
    pairs_dic = {}

