import os
import argparse

def convert_roam_journal_to_hepta(dir_roam_export: str) -> None:
    # Get list of journal files
    # Create output directory
    # Copy Roam journal files to output directory
    # Rename Roam journal files to Heptabase file format
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roam_export_dir", '-r',
                        help='Path to exported Roam MD files, unzipped',
                        required=True,
                        type=str)
    # parser.add_argument("--output_dir", '-o',
    #                     help='Path to output converted journal files. '
    #                          'If none, script generates a folder next to '
    #                          'input folder.',
    #                     required=False,
    #                     default='',
    #                     type=str)
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parse_args()
    convert_roam_journal_to_hepta(args['roam_export_dir'])
