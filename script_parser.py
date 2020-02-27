import csv

FILE_NAME = "data\\HP1full_script.txt"

file_obj = open(FILE_NAME, "r")
def get_data():
    return file_obj.read()


raw_data = get_data().split("\n")
scene_flag = False
with open("HP1.csv", 'w', newline='') as f:
    w = csv.writer(f)
    for line in raw_data:
        if line == "":
            continue
        line = line.split(":")
        if line[0] == "Scene":
            scene_flag = True
            continue
        if scene_flag:
            scene_flag = False
            continue
        if len(line[0].split(" ")) > 1:
            continue
        try:
            speaker = line[0]
            quote = ":".join(line[1:])
            if quote[0] == " ":
                quote = quote[1:]
            w.writerow([speaker, quote])
        except:
            print(line)


file_obj.close()

