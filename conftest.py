import pytest
from . import dotdictionary

DD = dotdictionary.DotDictionary

testdict = {
    "val01": 0,
    "Level1": {
        "val11": 1,
        "val12": 2,
        "Level2": {
            "Level3": {
                "val31": 5,
                "val32": 8,
                "Level4": {
                    "val41": 9,
                    "Level5": {
                        "val51": 10,
                        "val52": 11
                    }
                },
            },
            "val21": 3,
            "val22": 4,
            "list2": [1, 2, 3, 4, 5]
        }
    }
}

@pytest.fixture
def dotdictobj():
    n = DD()
    n.from_dict(testdict)
    return n
