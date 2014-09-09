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


def denormalize_name(name):
    """ Perform the reverse of normalize_name (this may lose information) """
    name = name[0].lower() + name[1:]
    result = []
    i = 0
    start = 0
    while i < len(name):
        if name[i].isupper():
            result.append(name[start:i].lower())
            start = i
        i += 1
    result.append(name[start:].lower())

    return '_'.join(result)


def privatize_name(name):
    """ Create the private version of a name. """
    if name[-1] != '_':
        name += '_'
    return name


def publicize_name(name, normalize=False):
    """ Create the public version of a name. """
    if normalize:
        name = normalize_name(name)
    if name[-1] == '_':
        return name[:-1]
    else:
        return name


def classify_name(name, normalize=False):
    """ Create a version of a name that can be used as a class name. """
    if normalize:
        name = normalize_name(name)
    return publicize_name(name[0].upper() + name[1:])


def varify_name(name, normalize=False):
    """ Create a version of a name that can be used as a variable. """
    if normalize:
        name = normalize_name(name)
    return publicize_name(name[0].lower() + name[1:])


def methodize_name(name, static=False):
    """ Create a version of a name that can be used as a method name. """
    return name[0].lower() + name[1:]


def fileize_name(name):
    """ Create a version of a name that can be used in a filename. """
    return normalize_name(name).lower()
