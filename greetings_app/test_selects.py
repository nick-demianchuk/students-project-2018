from app import *
from mock import patch


class SimpleTestData(object):
    def __init__(self, name, counter):
        self.name = name
        self.counter = counter


simple_test_data = [SimpleTestData('looser', 1),
                    SimpleTestData('winner', 100)
                    ]


def test_max():
    assert 'winner' == get_max(simple_test_data).name


def test_get_all():
    with patch('app.Stranger') as model_mock:
        query_all = model_mock.query.all
        get_all_strangers()
        query_all.assert_called_once_with()
