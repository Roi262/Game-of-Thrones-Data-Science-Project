import csv
from os import listdir
from os.path import isfile, join


def parse_timestamp(line):
    # timestamp on srt file is formatted like 
    # "00:01:55,418 --> 00:01:58,420"
    l = line.split(" ")
    return l[0], l[2].strip()


def clean(line):
    if line.startswith("- "):
        line = line[2:]
    return line.strip().replace("</i>", "").replace("<i>", "").replace("\"", "").strip()


def write_to_csv(writer, num, times, line):
    writer.writerow([num, times[0], times[1], line])


def parse_srt_file(path):
    """ Turns srt file to csv with fields linenum, start_time, end_time, line """
    output_file_name = path.split('\\')[-1].replace(".srt", ".csv")

    with open(path, 'r') as s, open(output_file_name, 'w') as o:
        output_writer = csv.writer(o, delimiter=';')
        line = s.readline()
        while line:
            while not line.strip():
                line = s.readline()
            num = line.strip()
            line = s.readline().strip()
            times = parse_timestamp(line)
            l1 = s.readline()
            write_to_csv(output_writer, num, times, clean(l1))
            l2 = s.readline().strip()
            if l2:
                write_to_csv(output_writer, num, times, clean(l2))
                l3 = s.readline().strip()
                if l3:
                    write_to_csv(output_writer, num, times, clean(l3))
                    s.readline()
            line = s.readline()


# Finds all files in my_path and runs them through parse_srt_file
my_path = "C:\\Users\\Tamar 2\\Dropbox\\uni\\מחט\\final project\\data\\GoT srt files"
all_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
for p in all_files:
    parse_srt_file(my_path + "\\" + p)

