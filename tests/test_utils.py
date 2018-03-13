"""Utility functions tests."""
from change_license import get_years_string
import datetime


def test_years_string_formatter():
    """Test copyright years string formatter."""
    curr_year = str(datetime.date.today().year)
    assert get_years_string('2013') == '2015-' + curr_year
    assert get_years_string('2015') == '2015-' + curr_year

    # Single date if it's current year
    assert get_years_string('2018') == curr_year
    assert get_years_string('2030') == '2030'  # Date from future?
    assert get_years_string('2014', lower_year='2013', upper_year='2020') == \
        '2014-2020'
    assert get_years_string('2019', lower_year='2013', upper_year='2020') == \
        '2019-2020'
    assert get_years_string('2012', lower_year='2013', upper_year='2020') == \
        '2013-2020'
