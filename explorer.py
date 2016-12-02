import re

def json_get(json, json_path):
    """Get a value based on a json_path key
    """
    for key in json_path:
        try:
            json = json[key]
        except (TypeError, KeyError):
            return
    return json

def get_escaped_keys(json, sep, escape):
    return [k.replace(sep, escape+sep) for k in json.keys()]

def walk(json, sep='/', escape='MOZESCAPE', include_escape=False):
    """Walk a json blob, returning a list of all key paths
    """
    match_reg = r'(?<!{}){}'.format(escape, sep)
    explored, unexplored = set(), set(get_escaped_keys(json, sep, escape))

    while unexplored:
        next = unexplored.pop()
        explored.add(next)

        #don't match on escape chars
        next_path = re.split(match_reg, next)

        #remove escape chars before following path
        val = json_get(json, [np.replace(escape, '') for np in next_path])

        if type(val) is dict:
            unexplored |= set([sep.join((next, k)) for k in get_escaped_keys(val, sep, escape)])

    map_func = lambda x: x if include_escape else x.replace(escape, '')
    return [map_func(x) for x in sorted(list(explored), key=lambda x: len(re.split(match_reg, x)))]

def find(json, needle):
    """Returns all paths containing needle 
    """
    return [k for k in walk(json) if needle in k]
