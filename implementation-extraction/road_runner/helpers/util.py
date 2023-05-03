def flatten(iterable: []) -> []:
    """
    Flatten a list.
    :param iterable: the list to be flattened.
    """
    # These types won't considered a sequence or generally a container
    exclude = str, bytes

    for i in iterable:
        try:
            if isinstance(i, exclude):
                raise TypeError
            iter(i)
        except TypeError:
            yield i
        else:
            yield from flatten(i)
