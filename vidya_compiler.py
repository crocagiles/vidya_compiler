from pathlib import Path
from datetime import date, datetime
from moviepy.editor import concatenate_videoclips, VideoFileClip
import logging

logging.basicConfig(level=logging.INFO)

def get_vids_from_date(dir_hunt, date_to_pull_from):
    vids = dir_hunt.glob('*.MP4')  # hard coded to mp4, that's what nvidia highlights writes out

    vids_from_date = []
    for vid in vids:
        created = vid.stat().st_ctime
        created_fmt = datetime.fromtimestamp(created)

        if date_to_pull_from == created_fmt.date():
            vids_from_date.append(vid)

    if len(vids_from_date) == 0:
        logging.error(f'No videos were found from date {str(date_to_pull_from)}. No video will be written.')
        quit()

    return vids_from_date


def main(dir_hunt, date_to_pull_from):
    dir_hunt_p = Path(dir_hunt)
    vids_list_p = get_vids_from_date(dir_hunt_p, date_to_pull_from)
    vids_list = [VideoFileClip(str(i)) for i in vids_list_p]

    # Configure output location and filename
    dir_output = dir_hunt_p / "compiled_videos"
    if not dir_output.exists():
        dir_output.mkdir()
    fname_out = f'{str(date_to_pull_from)}_compilation.MP4'
    full_out = dir_output / fname_out

    # Compile video
    num_vids = len(vids_list)
    logging.info(f'Concatenating {num_vids} clip(s)')

    final_clip = concatenate_videoclips(vids_list)
    final_clip.write_videofile(str(full_out))

    return


if __name__ == '__main__':
    today = date.today()

    # Configure for your system :)
    dir_hunt = r'C:\Users\giles\Videos\Hunt  Showdown'  # Location where your hunt clips are stored
    custom_date = datetime(2020, 12, 2).date()  # Use a custom date if compiling video from a day in the past.

    # main(dir_hunt=dir_hunt, date_to_pull_from=today)  # Compile videos from today
    main(dir_hunt=dir_hunt, date_to_pull_from=custom_date)  # Compile videos from "custom_date"
