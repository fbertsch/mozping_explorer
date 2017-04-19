import re

re_special_chars = {'.', '\\', '$', '*', '^'}

def json_get(json, json_path):
    """Get a value based on a json_path key
    """
    for key in json_path:
        try:
            json = json[key]
        except (TypeError, KeyError):
            return
    return json

def get_escaped_keys(json, sep, escape, prepend=None):
    if prepend is None:
        prepend = []
    return {tuple([p for p in prepend] + [k.replace(sep, escape+sep)]) for k in json.keys()}

def walk(json, sep='/', escape='MOZESCAPE', include_escape=False):
    """Walk a json blob, returning a list of all key paths
    """
    #todo: allow sep be multiple chars, escape any special chars in escape

    explored, unexplored = set(), get_escaped_keys(json, sep, escape)

    while unexplored:
        next = unexplored.pop()
        explored.add(next)
        next_val = json_get(json, [n.replace(escape, '') for n in next])

        if type(next_val) is dict:
            unexplored |= get_escaped_keys(next_val, sep, escape, prepend=next)

    map_func = lambda x: x if include_escape else x.replace(escape, '')
    return {map_func(sep.join(x)) for x in explored}

def find(json, needle, case=False):
    """Returns all paths containing needle 

    :param json, the haystack to search
    :param needle, the string to find
    :param case, whether this is case sensitive (default False)
    """
    return {k for k in walk(json) if (needle in k if case else needle.lower() in k.lower())}
