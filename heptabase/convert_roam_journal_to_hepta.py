import argparse
import datetime
import os
import re
import shutil
from typing import Optional

import pandas as pd

MONTH_NUMBER_DICT = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


def get_list_of_journal_files(dir_roam_export):
    # Get list of journal files
    objs = os.listdir(dir_roam_export)
    files = [o for o in objs
             if os.path.isfile(os.path.join(dir_roam_export, o))]
    regex_str = '\w+\s[0-9]{1,2}[a-z]{2}[,]\s[0-9]{4}.md'
    r = re.compile(regex_str)
    j_files = list(filter(r.match, files))
    return j_files


def create_output_dir(dir_roam_export) -> str:
    # Create output directory
    parent_path, dir_name = os.path.split(dir_roam_export)
    out_dir_name = dir_name + '-converted'
    out_dir_path = os.path.join(parent_path, out_dir_name)
    if os.path.exists(out_dir_path):
        # print(f"Warning: converted files already exist. "
        #       f"Please delete dir: {out_dir_path}. Then re-run.")
        # exit(0)
        shutil.rmtree(out_dir_path)
    os.makedirs(out_dir_path)
    return out_dir_path


def setup_df_and_extract_dates(j_files, dir_roam_export):
    # Setup dataframe
    df = pd.DataFrame({'roam_filename': j_files})
    df['roam_filepath'] = df['roam_filename'].apply(
        lambda f: os.path.join(dir_roam_export, f))

    # Extract date and generate new names
    df['datetime'] = df['roam_filename'].apply(extract_date_time)
    df['hepta_filename'] = df['datetime'].apply(hepta_name_from_date)
    return df


def copy_journal_files(df: pd.DataFrame, out_dir_path: str) -> None:
    # Copy journal files from Roam dir to out dir
    df['roam_dest_filepath'] = df['roam_filename'].apply(
        lambda f: os.path.join(out_dir_path, f))
    for i, row in df.iterrows():
        if row['datetime']:
            shutil.copyfile(row['roam_filepath'], row['roam_dest_filepath'])


def rename_roam_to_hepta_format(df: pd.DataFrame, out_dir_path: str) -> None:
    # Rename Roam journal files to Heptabase file format
    df['hepta_filepath'] = df['hepta_filename'].apply(
        lambda f: os.path.join(out_dir_path, f))
    for i, row in df.iterrows():
        if row['datetime']:
            os.rename(row['roam_dest_filepath'], row['hepta_filepath'])


def extract_date_time(filename: str) -> Optional[datetime.datetime]:
    datetime_out = None
    regex_str = '(\w+)\s([0-9]{1,2})[a-z]{2}[,]\s([0-9]{4}).md'
    re_date_elems = re.search(regex_str, filename)
    if re_date_elems:
        month_num = MONTH_NUMBER_DICT[re_date_elems.group(1)]
        datetime_out = datetime.date(int(re_date_elems.group(3)),
                                     int(month_num),
                                     int(re_date_elems.group(2)))
    return datetime_out


def hepta_name_from_date(date: datetime) -> str:
    if date:
        ymd_format = date.isoformat()
        hepta_format = ymd_format + ".md"
    else:
        hepta_format = ""
    return hepta_format


def convert_roam_journal_to_hepta(dir_roam_export: str) -> None:
    j_files = get_list_of_journal_files(dir_roam_export)
    out_dir_path = create_output_dir(dir_roam_export)
    df = setup_df_and_extract_dates(j_files, dir_roam_export)
    copy_journal_files(df, out_dir_path)
    rename_roam_to_hepta_format(df, out_dir_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roam_export_dir", '-r',
                        help='Path to exported Roam MD files, unzipped',
                        required=True,
                        type=str)
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parse_args()
    convert_roam_journal_to_hepta(args['roam_export_dir'])
