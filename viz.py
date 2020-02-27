import matplotlib.pyplot as plt
from collections import defaultdict


def trim_dict(my_dict, threshold):
    new_dict = defaultdict(int)
    for v in my_dict:
        if my_dict[v] > threshold:
            new_dict[v] = my_dict[v]
    return new_dict


def dict_to_bar_graph(my_dict, head=0):
    if head > 0:
        my_dict = trim_dict(my_dict, head)
    my_dict = {k: v for k, v in sorted(my_dict.items(), key=lambda item: item[1], reverse=True)}
    plt.bar(range(len(my_dict)), list(my_dict.values()), align='center')
    plt.xticks(range(len(my_dict)), list(my_dict.keys()), rotation=45)
    plt.show()

