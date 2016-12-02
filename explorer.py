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

def walk(json, sep='/', escape='MOZESCAPE'):
    """Walk a json blob, returning a list of all key paths
    """
    explored, unexplored = set(), set(json.keys())
    
    while unexplored:
        next = unexplored.pop()
        explored.add(next)
         
        #don't match on escape chars
        next_path = re.split(r'(?<!{}){}'.format(escape, sep), next)
        
        #remove escape chars before following path
        val = json_get(json, [np.replace(escape, '') for np in next_path])

        if type(val) is dict:
            unexplored |= set([sep.join((next, k.replace(sep, escape+sep))) for k in val.keys()])
    
    return sorted(list(explored), key=lambda x: x.count(sep))

def find(json, key):
    """Returns all key paths ending in key
    """
    return [k for k in walk(json) if k.endswith(key)]
    
