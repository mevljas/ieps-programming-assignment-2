import sys

from road_runner.helpers.data_processor import parse_html


def get_printable_iterator(iterator: [str]) -> str:
    """
    Generate printable string presentation of the iterator.
    :param iterator: roadrunner generated iterator.
    :return: printable string presentation of the iterator.
    """
    buffer = "( "
    for token in iterator:
        if token[0] == "head_tag":
            buffer += "".join(["<", token[1], ">"])
        elif token[0] == "tail_tag":
            buffer += "".join(["</", token[1], ">"])
        elif token[0] == "optional":
            buffer += token[1] + ""
        else:
            buffer += token[1]

    return buffer + " )+\n"


def get_printable_wrapper(wrapper: [str]) -> str:
    """
    Generate printable string presentation of the wrapper.
    :param wrapper: roadrunner generated wrapper.
    :return: printable string presentation of the wrapper.
    """
    buffer = ""

    for token in wrapper:
        if token[0] == "head_tag":
            buffer += "".join(["<", token[1], ">\n"])
        elif token[0] == "tail_tag":
            buffer += "".join(["</", token[1], ">\n"])
        elif token[0] == "optional":
            buffer += token[1] + "\n"
        elif token[0] == "iterator":
            buffer += get_printable_iterator(token[1])
        else:
            buffer += token[1] + "\n"

    return buffer


def compare_tokens(first: [str], second: [str]) -> bool:
    """
    Compare two tokens and returns True if they're equal and False otherwise.
    :param first: first token to be compared.
    :param second: second token to be compared.
    :return: True if the tokens are equal and False otherwise.
    """
    if first[0] == second[0] and first[1] == second[1]:
        return True
    elif first[0] == "optional" and first[1][1:-2] == second[1]:
        print("Optional token matching.", file=sys.stderr)
        return True

    return False


def find_iterator_end(tokens: [str], start_position: int) -> int | None:
    """
    Find the position of the previous terminal tag with the same value.
    :param tokens: a list of page tokens.
    :param start_position: first possible tag position.
    :return: tag position if found, None otherwise.
    """
    i = start_position
    while i < len(tokens):
        if tokens[i][0] == "tail_tag" and tokens[i][1] == tokens[start_position][1]:
            return i
        i += 1

    return None


def find_iterator_start(tokens: [str], start_position: int) -> int | None:
    """
    Find the position of the previous start tag with the same value.
    :param tokens: a list of page tokens.
    :param start_position: first possible tag position.
    :return: tag position if found, None otherwise.
    """
    i = start_position
    while i > 0:
        if tokens[i][0] == "head_tag" and tokens[i][1] == tokens[start_position][1]:
            return i
        i -= 1

    return None


def wrapper_generalization_iterator(wrapper: [str], tag_mismatch: str, internal_wrapper: [str]) -> [str]:
    """
    Generalize the wrapper by incorporating the iterator.
    :param wrapper: currently generated wrapper.
    :param tag_mismatch: tag that caused the mismatch.
    :param internal_wrapper: iterator square.
    :return: generalized wrapper.
    """
    i = len(wrapper) - 1
    iterator_start = None

    while i > 0:
        # Skip optional tags.
        # TODO: Is this necessary?
        while i > 0 and wrapper[i][0] == "optional":
            i -= 1

        # Find the previous terminal tag of the same type.
        if wrapper[i][0] == "tail_tag" and wrapper[i][1] == tag_mismatch:
            # Previous terminal tag found.
            while i > 0:
                # Find the start tag.
                if wrapper[i][0] == "head_tag" and wrapper[i][1] == tag_mismatch:
                    iterator_start = i
                    i -= 1
                    break
                i -= 1
        else:
            break

    if iterator_start is None:
        # Wrapper generalization failed.
        return wrapper

    # New iterator found.
    # Remove data from the wrapper from iterator start onwards.
    wrapper = wrapper[:iterator_start]
    new_iterator = ["iterator", internal_wrapper]
    wrapper.append(new_iterator)
    return wrapper


def wrapper_generalization_optional_field(wrapper: [str], token: [str]) -> [str]:
    """
    Generalize the wrapper by incorporating optional fields.
    :param wrapper: currently generated wrapper.
    :param token: page token.
    :return: generalized wrapper.
    """
    wrapper.append(["optional", " ".join(["( <", token[1], "/> )?"])])
    return wrapper


def roadrunner(first_page: [str], second_page: [str], first_index: int, second_index: int, wrapper: [str]) -> [str]:
    """
    Runs the roadrunner algorithm on the provided pages.
    :param first_page: first html page.
    :param second_page: second html page.
    :param first_index: current pointer index on the first page.
    :param second_index: current pointer index on the second page.
    :param wrapper: current generated solution wrapper.
    :return: generated wrapper.
    """
    # Recursive end condition.
    if first_index == len(first_page) and second_index == len(second_page):
        # The algorithm is finished.
        return wrapper

    page1_token = first_page[first_index]
    page2_token = second_page[second_index]

    # Check if tokens are equal.
    if compare_tokens(page1_token, page2_token):
        # If the tokens are equal, add token to the solution and go deeper.
        wrapper.append(page1_token)
        return roadrunner(first_page=first_page,
                          second_page=second_page,
                          first_index=first_index + 1,
                          second_index=second_index + 1,
                          wrapper=wrapper)
    else:
        # If the tokens aren't equal there has been a mismatch.
        # Check whether both tokens are database fields.
        if page1_token[0] == "data" and page2_token[0] == "data":
            # If both tokens are database fields it's a string mismatch.
            wrapper.append(["data", "#PCDATA"])
            return roadrunner(first_page, second_page, first_index + 1, second_index + 1, wrapper)
        else:
            # If at least one of the tokens isn't a database field, it's a tag mismatch.
            # check for iterators
            # square location by terminal–tag search

            # Get previous tokens.
            previous_page1_token = first_page[first_index - 1]
            previous_page2_token = second_page[second_index - 1]
            iterator_found = False

            # Check if the previous token on the first page is a terminal tag and
            # matches the current token on the first page.
            if previous_page1_token[0] == "tail_tag" and page1_token[0] == "head_tag" \
                    and previous_page1_token[1] == page1_token[1]:
                # possible iterator discovered on the first page.
                # Verify with square matching.
                # confirm existence of equal terminal tag.
                previous_terminal_position = find_iterator_end(tokens=first_page, start_position=first_index)

                if previous_terminal_position is not None:
                    previous_start_position = find_iterator_start(tokens=first_page,
                                                                  start_position=first_index - 1)

                    if previous_start_position is not None:
                        prev_square = first_page[previous_start_position:first_index]
                        square = first_page[first_index:previous_terminal_position + 1]
                        internal_wrapper = roadrunner(first_page=prev_square,
                                                      second_page=square,
                                                      first_index=0,
                                                      second_index=0,
                                                      wrapper=[])

                        if internal_wrapper is not None:
                            new_wrapper = wrapper_generalization_iterator(wrapper=wrapper,
                                                                          tag_mismatch=page1_token[1],
                                                                          internal_wrapper=internal_wrapper)
                            iterator_found = True
                            return roadrunner(first_page=first_page,
                                              second_page=second_page,
                                              first_index=previous_terminal_position + 1,
                                              second_index=second_index,
                                              wrapper=new_wrapper)

            # Check if the previous token on the second page is a terminal tag and
            # matches the current token on the second page.
            elif previous_page2_token[0] == "tail_tag" and page2_token[0] == "head_tag" \
                    and previous_page2_token[1] == page2_token[1]:
                # possible iterator discovered on the second page.
                # Verify with square matching.
                # confirm existence of equal terminal tag.
                previous_terminal_position = find_iterator_end(tokens=second_page, start_position=second_index)

                if previous_terminal_position is not None:
                    # confirm existence of equal start tag.
                    previous_start_position = find_iterator_start(tokens=second_page,
                                                                  start_position=second_index - 1)

                    if previous_start_position is not None:
                        prev_square = second_page[previous_start_position:second_index]
                        square = second_page[second_index:previous_terminal_position + 1]
                        internal_wrapper = roadrunner(first_page=prev_square,
                                                      second_page=square,
                                                      first_index=0,
                                                      second_index=0,
                                                      wrapper=[])

                        if internal_wrapper is not None:
                            wrapper = wrapper_generalization_iterator(wrapper=wrapper,
                                                                      tag_mismatch=page2_token[1],
                                                                      internal_wrapper=internal_wrapper)
                            iterator_found = True
                            return roadrunner(first_page=first_page,
                                              second_page=second_page,
                                              first_index=first_index,
                                              second_index=previous_terminal_position + 1,
                                              wrapper=wrapper)

            # Check for optionals.
            if not iterator_found:
                # Optional pattern location by cross–search.

                # Check whether the first page contains an optional pattern.
                if compare_tokens(first_page[first_index + 1], page2_token):
                    # Skipping an optional pattern works, generalize wrapper and proceed.
                    wrapper = wrapper_generalization_optional_field(wrapper=wrapper, token=page1_token)
                    return roadrunner(first_page, second_page, first_index + 1, second_index, wrapper)

                # Check whether the second page contains an optional pattern.
                elif compare_tokens(page1_token, second_page[second_index + 1]):
                    # Skipping an optional pattern works, generalize wrapper and proceed.
                    wrapper = wrapper_generalization_optional_field(wrapper=wrapper, token=page2_token)
                    return roadrunner(first_page, second_page, first_index, second_index + 1, wrapper)
                else:
                    print("Error skipping optional pattern.", file=sys.stderr)
                    return None


def road_runner(first_html: str, second_html: str) -> None:
    """
    Runs the roadrunner algorithm on the provided pages.
    :param first_html: HTML of the first page.
    :param second_html: HTML of the second page.
    """
    first_page, second_page = parse_html(first_html=first_html, second_html=second_html)
    wrapper = roadrunner(first_page, second_page, 0, 0, [])
    solution = get_printable_wrapper(wrapper=wrapper)
    print(solution)
