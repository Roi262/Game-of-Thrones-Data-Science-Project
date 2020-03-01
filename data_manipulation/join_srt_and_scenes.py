import pandas as pd
import ast

Path = "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E03 The Queen_s Justice.csv"

offsets = {
        1: {
                1: {"path": "../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x01 - Winter is Coming.720p HDTV.en.csv", "offset":-30},
                2: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x02 - The Kingsroad.HDTV.en.csv", "offset":-35},
                3: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x03 - Lord Snow.HDTV.en.csv", "offset": 0},
                4: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x04 - Cripples  Bastards  and Broken Things.HDTV.en.csv", "offset":0},
                5: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x05 - The Wolf and the Lion.HDTV.en.csv", "offset":0},
                6: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x06 - A Golden Crown.HDTV.en.csv", "offset":0},
                7: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x07 - You Win or You Die.HDTV.en.csv", "offset":90},
                8: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x08 - The Pointy End.HDTV.en.csv", "offset":0},
                9: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x09 - Baelor.HDTV.en.csv", "offset":-34},
                10: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 1x10 - Fire and Blood.HDTV.FQM.en.csv", "offset":-29}},
           2: {
               1: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x01 - The North Remembers.720p.BluRay.REWARD.en.csv", "offset":-35},
               2: {"path": "../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x02 - The Night Lands.HDTV.fqm.en.csv", "offset":0},
               3: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x03 - What is Dead May Never Die.HDTV.fqm.en.csv", "offset":0},
               4: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x04 - Garden of Bones.HDTV.FQM.en.csv", "offset":0},
               5: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x05 - The Ghost of Harrenhal.HDTV.2HD.en.csv", "offset":0},
               6: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x06 - The Old Gods and the New.720p.BluRay.DEMAND.en.csv", "offset":0},
               7: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x07 - A Man Without Honor.720p.BluRay.DEMAND.en.csv", "offset":0},
               8: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x08 - The Prince of Winterfell.720p.BluRay.DEMAND.en.csv", "offset":0},
               9: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x09 - Blackwater.720p.BluRay.DEMAND.en.csv", "offset":0},
               10: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 2x10 - Valar Morghulis.720p.BluRay.DEMAND.en.csv", "offset":0}},
           3: {
               1: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 3x01 - Valar Dohaeris.HDTV.x264-2HD.en.csv", "offset":0},
               2: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 3x02 - Dark Wings  Dark Words.HDTV.en.csv", "offset":0},
               3: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 3x03 - Walk of Punishment.HDTV.x264-PROPER 2HD.en.csv", "offset":90},
               4: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 3x04 - And Now His Watch is Ended.720p HDTV.en.csv", "offset":90},
               5: {"path":"../data/Game of Thrones/STR converted to CSV/ori_episodes/Game of Thrones - 3x05 - Kissed by Fire.HDTV.en.csv", "offset":90},
                6: {"path": "../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 3x06 - The Climb.HDTV.2HD.en.csv", "offset": 103},
                7: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 3x07 - The Bear and the Maiden Fair.HDTV.x264-2HD.en.csv", "offset": 164},
                8: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 3x08 - Second Sons.480p HDTV.EVOLVE.en.csv", "offset": 102},
                9: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 3x09 - The Rains of Castamere.HDTV.x264-EVOLVE.en.csv", "offset": 102},
                10: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 3x10 - Mhysa.HDTV.evolve.en.csv", "offset": 110}
                },
           4: {
               1: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x01 - Two Swords.1080i.HDTV.CtrlHD.en.csv", "offset": 120},
               2: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x02 - The Lion and the Rose.720p HDTV.2HD.HI.en.csv", "offset": -2},
               3: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x03 - Breaker of Chains.720p HDTV.en.csv", "offset": 87},
               4: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x04 - Oathkeeper.1080i.HDTV.CtrlHD.en.csv", "offset": 98},
               5: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x05 - First of His Name.1080i.HDTV.CtrlHD.en.csv", "offset": 106},
               6: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x06 - The Laws of Gods and Men.1080i.HDTV.CtrlHD.en.csv", "offset": 97},
               7: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x07 - Mockingbird.1080i.HDTV.CtrlHD.en.csv", "offset": 98},
               8: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x08 - The Mountain and the Viper.1080i.HDTV.CtrlHD.en.csv", "offset": 27},
               9: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x09 - The Watchers on the Wall.720p HDTV.KILLERS.en.csv", "offset": 60},
               10: {"path":"../data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x10 - The Children.1080i.HDTV.CtrlHD.en.csv", "offset": 62}
               },
            5: {
                1: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E01 The Wars To Come.csv", "offset": -213},
                2: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E02 The House Of Black And White.csv", "offset": -96},
                3: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E03 High Sparrow.csv", "offset": -90},
                4: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E04 Sons Of The Harpy.csv", "offset": -94},
                5: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E05 Kill The Boy.csv", "offset": -104},
                6: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E06 Unbowed, Unbent, Unbroken.csv", "offset": -106},
                7: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E07 The Gift.csv", "offset": -106},
                8: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E08 Hardhome.csv", "offset": -102},
                9: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E09 The Dance Of Dragons.csv", "offset": -148},
                10: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S05E10 Mother_s Mercy.csv", "offset": -195}
                },
            6: {
                1: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E01 The Red Woman.csv", "offset": -308},
                2: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E02 Home.csv", "offset": -178},
                3: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E03 Oathbreaker.csv", "offset": -207},
                4: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E04 Book of the Stranger.csv", "offset": -195},
                5: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E05 The Door.csv", "offset": -200},
                6: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E06 Blood of My Blood.csv", "offset": -184},
                7: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E07 The Broken Man.csv", "offset": -176},
                8: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E08 No One.csv", "offset": -251},
                9: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E09 Battle of the Bastards.csv", "offset": -171},
                10: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S06E10 The Winds of Winter.csv", "offset": -218}
                },
            7: {
                1: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E01 Dragonstone.csv", "offset": -79},
                2: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E02 Stormborn.csv", "offset": -77},
                3: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E03 The Queen_s Justice.csv", "offset":  33},
                4: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E04 The Spoils Of War.csv", "offset": -33},
                5: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E05 Eastwatch.csv", "offset": -34},
                6: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E06 Beyond The Wall.csv", "offset": -34},
                7: {"path": "../data/Game of Thrones/STR converted to CSV/tamar_episodes/Game Of Thrones S07E07 The Dragon And The Wolf.csv", "offset": -69}
                }
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

    # for lines in scenes_lines:
    #     print(lines)

    # scenes_lines_dic[(season, episode)] = scenes_lines
    return scenes_lines

def get_scenes_lines_dic():
    scenes_lines_dic = {}
    for season in offsets.keys():
        if not season == 4:
            continue
        for episode in offsets[season].keys():
            scenes_lines_dic[(season, episode)] = join_scene_with_srt(
                offsets[season][episode]["path"],
                "../data/Game of Thrones/scenes_timestamps.csv",
                offsets[season][episode]["offset"], season, episode)
    return scenes_lines_dic




# if __name__ == "__main__":
    # scenes_lines_dic[(season, episode)] = join_scene_with_srt(
    #     "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/STR converted to CSV/rois_episodes/Game of Thrones - 4x10 - The Children.1080i.HDTV.CtrlHD.en.csv",
    #     "/Users/roiaharonson/Code/UNI CODE/INTRO TO DATA SCIENCE/Final Project/data/Game of Thrones/scenes_timestamps.csv",
    #     offsets[4][10], 4, 10)
