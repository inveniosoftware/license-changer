import filecmp
import os

from update_contributors import update_contributors


def test_setup_file_cleanup():
    """Test updating the AUTHORS.rst file.

    NOTE: This test is getting the contributors from license-changer
    reporitory. If there will be new people contributing to this repository,
    you might need to update the test/data/AUTHORS_out.rst file with that
    person's name.
    """

    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    output_file = os.path.join(data_folder, 'AUTHORS_out.rst')

    update_contributors('.')
    # update_contributors('.') will create AUTHORS.rst in the current directory
    assert filecmp.cmp(output_file, 'AUTHORS.rst')
    os.remove('AUTHORS.rst')
