def merge_dictionaries(original=None, new=None):
    """
    This will merge two dictionaries together, the original dictionary
    will be updated in memory.

    Keyword Arguments:
        original {dictionary} -- The original dictionary
        new {dictionary} -- The new dictionary
    """
    for key, val in new.iteritems():
        if isinstance(val, dict):
            if key in original:
                merge_dictionaries(original=original[key], new=val)
            else:
                original[key] = val
        else:
            if isinstance(val, list):
                if key in original:
                    val = val + original[key]
                else:
                    original[key] = val
            else:
                original[key] = val

