def camelcase(string):
    """convert a string from under_score to CamelCase"""
    result = []
    for token in string.split('_'):
        result.append(token[0].upper() + token[1:])
    return "".join(result)
