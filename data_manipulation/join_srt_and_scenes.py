import pandas as pd
import ast

offsets = {1: {1: -30, 2: -35, 3: 0, 4: 0, 5: 0, 6: 0, 7: 90, 8: 0, 9: -34, 10: -29},
           2: {1: -35, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
           3: {1: 0, 2: 0, 3: 90, 4: 90, 5: 90, 
                6: {"path": "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 3x06 - The Climb.HDTV.2HD.en.csv", "offset": 103},
                7: {"path":"", "offset": 164}, 8: 102, 9: 102, 10: 110},
           4: {1: 120, 2: -2, 3: 87, 4: 98, 5: 106, 6: 97, 7: 98, 8: 27, 9: 60, 10: 62},
           5: {1: -213, 2: -96, 3: -90, 4: -94, 5: -104, 6: -106, 7: -106, 8: -102, 9: -148, 10: -195},
           6: {1: -308, 2: -178, 3: -207, 4: -195, 5: -200, 6: -184, 7: -176, 8: -251, 9: -171, 10: -218},
           7: {1: -79, 2: -77, 3: 33, 4: -33, 5: -34, 6: -34, 7: -69}
           }


def scene_str_to_seconds(st: str) -> int:
    h, m, s = st.split(":")
    time = int(h) * 60 * 60 + int(m) * 60 + int(s)
    return time


def srt_str_to_seconds(st: str) -> int:
    st = st[:st.rfind(",")]
    h, m, s = st.split(":")
    time = int(h) * 60 * 60 + int(m) * 60 + int(s)
    return time


def join_scene_with_srt(srt_csv_filename: str, scene_csv_filename: str, scene_offset: int, season: int, episode: int):
    srt = pd.read_csv(srt_csv_filename, delimiter=";", header=None).to_numpy()
    scenes = pd.read_csv(scene_csv_filename, delimiter=",").to_numpy()

    # scenes_lines_dic = {}
    scenes_lines = []

    srt_index = 0

    for scene in scenes:
        scene_start_time = scene_str_to_seconds(scene[3]) + scene_offset
        scene_end_time = scene_str_to_seconds(scene[4]) + scene_offset
        scene_characters = ast.literal_eval(scene[5])
        characters = [dic['name'] for dic in scene_characters]

        if scene[0] != season or scene[1] != episode:
            continue

        scenes_lines.append(([], characters))

        in_scene = True
        while in_scene:
            if srt_index >= len(srt):
                break
            srt_line = srt[srt_index]
            srt_start = srt_str_to_seconds(srt_line[1])
            srt_end = srt_str_to_seconds(srt_line[2])

            if srt_start > scene_end_time:
                break
            elif srt_end > scene_end_time:
                break
            srt_index += 1
            scenes_lines[-1][0].append(srt_line[3])

    for lines in scenes_lines:
        print(lines)

    # scenes_lines_dic[(season, episode)] = scenes_lines
    return scenes_lines

def get_scenes_lines_dic():
    scenes_lines_dic = {}
    for season in offsets.keys():
        for episode in offsets[season].keys():
            scenes_lines_dic[(season, episode)] = join_scene_with_srt(
                offsets[season][episode]["path"],
                "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/scenes_timestamps.csv",
                offsets[season][episode]["offset"], season, episode)
    return scenes_lines_dic




if __name__ == "__main__":
    # scenes_lines_dic[(season, episode)] = join_scene_with_srt(
    #     "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x10 - The Children.1080i.HDTV.CtrlHD.en.csv",
    #     "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/scenes_timestamps.csv",
    #     offsets[4][10], 4, 10)
