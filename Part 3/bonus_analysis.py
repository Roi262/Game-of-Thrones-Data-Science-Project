from configure import *
# 1 pairs of characters who talk to each other most


RELEVENT_CHARACTERS = ALL_CHARACTERS_FORMAL

def get_both_char_lines():
    """returns one list of all lines character A says and
     another list of all lines character B says 
    """

# def score_function(k, nw) -> float:
#     """[summary]
    
#     Arguments:
#         k {[int]} -- number of rows in conversation
#         nw {[int]} -- total number of words in conversation
    
#     Returns:
#         float -- function score
#     """
#     word_count = 0
#     for row in rows_in_convo:
#         char1_lines, char2_lines = get_both_char_lines()

def get_sentiment(sentences):
    

def get_dialogues(data_path, char_1, char_2, conversation_thresh, noise= 2):
    """get all conversations of these 2 characters
    Arguments:
        data_path {[string]} -- path to csv file
        char_1 {[type]} -- Character 1
        char_2 {[type]} -- Character 2
        conversation_thresh {[int]} -- minimum amount of consecutive lines between 2 
        characters for the lines to be considered a conversation
        noise {[int]} -- maximum number of rows spoken by characters other than 1 and 2 which we 
        can disregard in the conversation
    Returns:
        conversations {2D array} -- an array of arrays of rows depicting conversations
    """
    with open(data_path, newline='') as f:
        data = csv.reader(f)
        conversations = []
        for i, row in enumerate(data):
            if i ==0: continue
            row_counter = 0
            conversation = []
            word_count = 0
            other_speaker_counter = 0
            while True:
                if row[SPEAKER] == char_1 or row[SPEAKER] == char_2:
                    word_count += len(row[LINE].split())
                    conversation.append((row[SPEAKER], row[LINE]))
                    row_counter += 1
                else:
                    other_speaker_counter += 1
                    if other_speaker_counter > noise:
                        break
            if row_counter >= conversation_thresh:
                sentiment = get_sentiment([tup[1] for tup in conversation])
                conversations.append((conversation, word_count, len(conversation), (char_1, char_2), sentiment))
    return conversations


def best_friends():
    # which characters talk most to each other
    pairs_dic = {}
    for pair in pairs_dic.keys():
        conversations = get_dialogues(data_path, pair[0], pair[1], conversation_thresh=6)



def plot_pair():
    pass

def plot_graph():
    for pair in character_pairs:
        plot_pair(pair)
    pass