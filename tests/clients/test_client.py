import pytest

from clients.client import Client


@pytest.mark.parametrize('display_name, items_available, pickup_interval, expected',
                         [
                             ('Oskroba', 8, '01.12 13:00-15:00',
                              'Oskroba\nAvailable: 8\nPickup time: 01.12 13:00-15:00\nSource: Client'),
                             ('Biedra', 0, '07.06 09:00-13:30',
                              'Biedra\nAvailable: 0\nPickup time: 07.06 09:00-13:30\nSource: Client')
                         ])
def test_form_msg(display_name, items_available, pickup_interval, expected):
    assert Client._form_msg(display_name, items_available, pickup_interval) == expected
