import pytest
from . import dotdictionary
DD = dotdictionary.DotDictionary

def test_toplevel(dotdictobj):
    print(type(dotdictobj))
    assert isinstance(dotdictobj.Level1, DD)
    assert dotdictobj.val01 == 0

def test_level2(dotdictobj):
    lev2 = dotdictobj.Level1.Level2
    assert isinstance(lev2, DD)
    assert lev2
    assert lev2.Level3
    assert lev2.val21 == 3
    assert lev2.val22 == 4
    assert lev2.val21 + lev2.val22 == 7

def test_level3(dotdictobj):
    lev3 = dotdictobj.Level1.Level2.Level3
    assert isinstance(lev3, DD)
    assert lev3.val31 == 5

def test_level4(dotdictobj):
    lev4 = dotdictobj.Level1.Level2.Level3.Level4
    assert isinstance(lev4, DD)
    assert lev4.val41 == 9

def test_level5(dotdictobj):
    lev5 = dotdictobj.Level1.Level2.Level3.Level4.Level5
    assert isinstance(lev5, DD)
    assert lev5.val51 == 10
    assert lev5.val52 == 11

def test_level2list(dotdictobj):
    list2 = dotdictobj.Level1.Level2.list2
    assert isinstance(list2, list)
    assert len(list2) == 5
    assert list2[0] == 1
    assert list2[4] == 5

def test_notsameinstance(dotdictobj):
    # instance of testdict
    t = dotdictobj
    # subdict
    subdict = {
        'test': 'instance',
        'list1': [0,1]
    }
    cptextsubdict = subdict['test']
    cplistsubdict = subdict['list1']
    t['subdict'] = subdict

    assert t['subdict'] == subdict
    assert t['subdict']['test'] == subdict['test'] == cptextsubdict == 'instance'
    assert t['subdict']['list1'] == subdict['list1'] == cplistsubdict == [0,1]



    t['subdict']['test'] = 'next'
    list = [1,2,3]
    t['subdict']['list'] = list

    assert cptextsubdict['test'] == 'next'
    assert cptextsubdict['list'] == list
    assert subdict['test'] == 'next'
    assert subdict['list'] == list

    new = DD()
    new.from_dict(t)

    # the string held in the dictionary should have been copied by value into the DotDictionary due to a string being
    #   a python immutable primitive and the "copy" is actually the instantiation of a new object with a new reference
    assert t["subdict"] == subdict
    assert new.subdict == subdict
    assert id(t["subdict"]) == id(subdict)
    # expected != because of n
    assert id(new.subdict) != id(subdict)

    # a list is added by reference since it is a mutable type. The id of the underlying object is the same
    assert new.subdict.list == list
    new.subdict.list.append(4) # change will be seen in all three referencing objects
    assert new.subdict.list[3] == 4
    assert t['subdict']['list'][3] == new.subdict.list[3] == subdict['list'][3]
    assert id(t['subdict']['list']) == id(new.subdict.list) == id(subdict['list'])



def test_sharedaccess(dotdictobj):
    # plain dictionary for testing
    olddict = {
        'name': "mary",
        'address': {
        'street': 'lamblane'
        }
    }

    # DotDict for testing
    newdotdict = DD()
    newdotdict.mod1 = DD()
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







