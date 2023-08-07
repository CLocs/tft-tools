import os
from unittest import TestCase
from shutil import rmtree

from heptabase.convert_roam_journal_to_hepta import \
    convert_roam_journal_to_hepta


class TestConvertJournal(TestCase):
    def setUp(self) -> None:
        self.test_base_path = os.path.abspath(os.path.dirname(__file__))
        self.journal_dir = os.path.join(self.test_base_path, 'roam-journal')
        self.out_dir = os.path.join(self.test_base_path,
                                    'roam-journal-converted')

    def tearDown(self) -> None:
        if os.path.exists(self.out_dir):
            rmtree(self.out_dir)

    def test_convert_filenames(self):
        convert_roam_journal_to_hepta(self.journal_dir)
        # Converted directory exists?
        self.assertTrue(os.path.exists(self.out_dir))
        # Check a converted file, eg, 1992-11-30.md
        conv_filepath1 = os.path.join(self.out_dir, '1992-11-30.md')
        self.assertTrue(os.path.exists(conv_filepath1))
