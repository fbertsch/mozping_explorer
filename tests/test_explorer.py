from mozping_explorer.explorer import find, walk

test_json = {'a': 1, 'b': {'c': 2}, 'd': 3}
test_json_escape = {'a/b': 1, 'b/c': {'c/d': 2}}

def test_walk():
    res = walk(test_json)
    assert res == {'a', 'b', 'd', 'b/c'}

def test_walk_with_sep():
    res = walk(test_json_escape)
    assert res == {'a/b', 'b/c', 'b/c/c/d'}

def test_walk_change_sep():
    res = walk(test_json, sep='.')
    assert 'b.c' in res

def test_walk_with_escape():
    escape = 'MOZESCAPE'
    res = walk(test_json_escape, include_escape=True, escape=escape)
    assert res == {'a{}/b'.format(escape), 'b{}/c'.format(escape), 'b{0}/c/c{0}/d'.format(escape)}

def test_find():
    assert find(test_json, 'a') == {'a'}

def test_find_multiple():
    assert find(test_json, 'b') == {'b', 'b/c'}
