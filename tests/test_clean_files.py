import filecmp
import os
from shutil import copyfile

from clean_files import clean_setup_file


def test_setup_file_cleanup():
    """Test cleaning setup.py file."""
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    input_file = os.path.join(data_folder, 'setup_in.py')
    output_file = os.path.join(data_folder, 'setup_out.py')
    setup_file = os.path.join(data_folder, 'setup.py')

    # Create the setup.py file from setup_in.py
    copyfile(input_file, setup_file)
    clean_setup_file(setup_file)
    assert filecmp.cmp(output_file, setup_file)
    os.remove(setup_file)
