import pytest
from dotdict import DotDict

def test_toplevel(dotdictobj):
    print(type(dotdictobj))
    assert isinstance(dotdictobj.Level1, DotDict)
    assert dotdictobj.val01 == 0

def test_level2(dotdictobj):
    lev2 = dotdictobj.Level1.Level2
    assert isinstance(lev2, DotDict)
    assert lev2
    assert lev2.Level3
    assert lev2.val21 == 3
    assert lev2.val22 == 4
    assert lev2.val21 + lev2.val22 == 7

def test_level3(dotdictobj):
    lev3 = dotdictobj.Level1.Level2.Level3
    assert isinstance(lev3, DotDict)
    assert lev3.val31 == 5

def test_level4(dotdictobj):
    lev4 = dotdictobj.Level1.Level2.Level3.Level4
    assert isinstance(lev4, DotDict)
    assert lev4.val41 == 9

def test_level5(dotdictobj):
    lev5 = dotdictobj.Level1.Level2.Level3.Level4.Level5
    assert isinstance(lev5, DotDict)
    assert lev5.val51 == 10
    assert lev5.val52 == 11

def test_level2list(dotdictobj):
    list2 = dotdictobj.Level1.Level2.list2
    assert isinstance(list2, list)
    assert len(list2) == 5
    assert list2[0] == 1
    assert list2[4] == 5

def test_sameinstance(testinstance):
    t = testinstance[0]
    inst = testinstance[1]
    new = DotDict()
    new.from_dict(t)

    assert t["instance"] == inst
    assert new.instance == inst
    # assert id(t["instance"]) == id(inst)
    # assert id(new.instance) == id(inst)

def test_sharedaccess(dotdictobj):
    # plain dictionary for testing
    olddict = {
        'name': "mary",
        'address': {
        'street': 'lamblane'
        }
    }

    # DotDict for testing
    newdotdict = DotDict()
    newdotdict.mod1 = DotDict()
    newdotdict.mod1.key1 = "configvar2"

    # parent DD
    ddo = dotdictobj

    # cases --

    # test adding newdotdict dictionary to parent DotDict object and referencing the ret with a new var newdotdict2
    olddictnew = ddo.add_dict('od', olddict)
    olddictnew2 = ddo.od.add_dict('od2', olddict)
    assert olddictnew == ddo.od
    ddo.od.name = "Maxine"
    assert olddictnew.name == "Maxine"
    assert ddo.od.od2 == olddictnew2
    assert olddictnew2.od2 == olddictnew
    # should not equal because the reference has been broken by the creation of a new object
    assert ddo.od.name != olddict['name']

    newdotdict2 = ddo.add_dict("nd", newdotdict)
    # test reference to the parent object.object
    newd = ddo.nd

    assert newdotdict == ddo.nd
    assert ddo.nd == newdotdict2
    ddo.nd.mod1.key1 = "configvar2a"
    assert ddo.nd.mod1.key1 == "configvar2a"
    assert newd.mod1.key1 == "configvar2a"
    assert newdotdict.mod1.key1 == "configvar2a"
    assert newdotdict2.mod1.key1 == "configvar2a"







