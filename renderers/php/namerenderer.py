def normalize_name(name):
    """ Change a name containing underscores and dots into a camel case var name """
    if '.' in name:
        name = name.rsplit('.', 1)[1]

    result = []
    if '_' not in name:
        return name

    i = 0
    while i < len(name):
        if name[i] == '_':
            if i != len(name) - 1:
                result.append(name[i + 1].upper())
                i += 1
            else:
                result.append('_')
        else:
            result.append(name[i])
        i += 1
    return ''.join(result)


def privatize_name(name):
    """ Create the private version of a name. """
    return normalize_name(name)


def publicize_name(name, normalize=False):
    """ Create the public version of a name. """
    return normalize_name(name)


def classify_name(name, normalize=False):
    """ Create a version of a name that can be used as a class name. """
    if name[0] == '$':
        name = name[1:]
    return normalize_name(name[0].upper() + name[1:])


def varify_name(name, normalize=False):
    """ Create a version of a name that can be used as a variable. """
    temp = name
    if name[0] != '$':
        name = '$' + name
    return normalize_name('$' + name[1].lower() + name[2:])


def methodize_name(name, static=False):
    """ Create a version of a name that can be used as a method name. """
    if name[0] == '$':
        name = name[1:]
    if static:
        return name[0].upper() + name[1:]
    else:
        return name[0].lower() + name[1:]


def fileize_name(name):
    """ Create a version of a name that can be used in a filename. """
    if name[0] == '$':
        name = name[1:]
    return name
