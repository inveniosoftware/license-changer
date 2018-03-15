import filecmp
import os
from shutil import copyfile

from update_travis import update_travis_config


def test_update_travis():
    """Test cleaning setup.py file."""
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    input_file = os.path.join(data_folder, 'travis_in.yml')
    output_file = os.path.join(data_folder, 'travis_out.yml')
    travis_file = os.path.join(data_folder, '.travis.yml')

    # Create the .travis.yml file from travis_in.yml
    copyfile(input_file, travis_file)
    update_travis_config(travis_file)
    assert filecmp.cmp(output_file, travis_file)
    os.remove(travis_file)
