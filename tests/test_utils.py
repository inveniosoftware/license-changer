"""Utility functions tests."""
from change_license import get_years_string, find_prefix_suffix
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


def test_find_prefix_suffix():
    start, end = '<!--', '-->'
    inside = 'GPL'

    t1 = '<!-- test -->stuff<!-- GPL -->morestuff'
    pref_suff = find_prefix_suffix(t1, start, end, inside)
    assert pref_suff == ('<!-- test -->stuff', 'morestuff')
    assert find_prefix_suffix('', start, end, inside) == None
    assert find_prefix_suffix('text but no tags', start, end, inside) == None
    assert find_prefix_suffix('<!-- tags but no inside word -->', start, end, inside) == None
    assert find_prefix_suffix('<!--GPL-->', start, end, inside) == ('', '')
    assert find_prefix_suffix('<!-- foo --> GPL outside tags', start, end, inside) == None
    assert find_prefix_suffix('GPL before tags <!-- foo -->', start, end, inside) == None
    assert find_prefix_suffix('<!-- GPL', start, end, inside) == None
    assert find_prefix_suffix('<!---->GPL -->', start, end, inside) == None
    assert find_prefix_suffix('<!--x--><!-- GPL --><!--y-->', start, end, inside) == ('<!--x-->', '<!--y-->')
