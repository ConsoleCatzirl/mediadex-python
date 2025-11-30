import pytest

from mediadex import util


test_user_defaults = {
    "option1": "foo",
    "option2": {
        "option3": "bar",
        "option4": "baz",
    },
    "option5": [
        "blort1",
        "blort2",
    ],
}

test_user_settings1 = {}
expected_user_settings1 = test_user_defaults

test_user_settings2 = {"invalid": "ignored"}
expected_user_settings2 = test_user_defaults

test_user_settings3 = {"option1": "test"}
expected_user_settings3 = test_user_defaults
expected_user_settings3["option1"] = "test"

test_user_settings4 = {"option2": {"option3": "test"}}
expected_user_settings4 = test_user_defaults
expected_user_settings4["option2"]["option3"] = "test"

test_user_settings5 = {"option5": ["test1", "test2"]}
expected_user_settings5 = test_user_defaults
expected_user_settings5["option5"] = ["test1", "test2"]


@pytest.mark.parametrize("user_settings,expected", [
    (test_user_settings1, expected_user_settings1),
    (test_user_settings2, expected_user_settings2),
    (test_user_settings3, expected_user_settings3),
    (test_user_settings4, expected_user_settings4),
    (test_user_settings5, expected_user_settings5),
])
def test_dict_merge(mocker, user_settings, expected):
    found = util.merge_dict(test_user_defaults, user_settings)
    assert found == expected
