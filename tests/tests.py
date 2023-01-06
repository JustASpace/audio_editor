import filecmp
import pathlib
import time
import unittest
import os
from backend.audio_editor_backend import AudioEditorBackEnd

test_backend = AudioEditorBackEnd()
test_dir = pathlib.Path.cwd()


class MyTestCase(unittest.TestCase):
    def test_creating_temp_folder(self):
        test_backend.create_temp_directory()
        self.assertTrue(os.path.isdir(test_backend.dirpath))

    def test_cut(self):
        test_backend.cut('test.mp3', 2, 2)
        time.sleep(3)
        output = pathlib.Path(test_backend.dirpath, 'test_cut.mp3')
        expected_output = pathlib.Path(test_dir, 'outputs', 'test_cut.mp3')
        result = filecmp.cmp(output, expected_output)
        self.assertTrue(result)

    def test_accelerate(self):
        test_backend.accelerate('test.mp3', 3)
        time.sleep(3)
        output = pathlib.Path(test_backend.dirpath, 'test_accelerated_by_3.mp3')
        expected_output = pathlib.Path(test_dir, 'outputs', 'test_accelerated_by_3.mp3')
        result = filecmp.cmp(output, expected_output)
        self.assertTrue(result)

    def test_reverse(self):
        pass

    def test_change_volume(self):
        pass

    def test_concat(self):
        pass

    def test_destroying_temp_folder(self):
        test_backend.remove_temp_directory()
        self.assertFalse(os.path.isdir(test_backend.dirpath))


if __name__ == '__main__':
    unittest.main()
