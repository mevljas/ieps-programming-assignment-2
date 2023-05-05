import sys

from road_runner.helpers.Token import Token
from road_runner.helpers.constants import TOKEN_TYPE, STRING_MISMATCH_FIELD
from road_runner.helpers.data_processor import prepare_data, get_printable_wrapper


def compare_tokens(first: Token, second: Token) -> bool:
    """
    Compare two tokens and returns True if they're equal and False otherwise.
    :param first: first token to be compared.
    :param second: second token to be compared.
    :return: True if the tokens are equal and False otherwise.
    """
    if first.token_type == second.token_type and first.value == second.value:
        return True
    elif first.token_type == TOKEN_TYPE.OPTIONAL and first.value[1:-2] == second.value:
        print("Optional token matching.", file=sys.stderr)
        return True
    # elif first.token_type == TOKEN_TYPE.DATABASE_FIELD and second.token_type == TOKEN_TYPE.DATABASE_FIELD:
    #     print("Database field matching.", file=sys.stderr)
    #     return True

    return False


def find_new_iterator_end(tokens: [Token], start_position: int) -> int | None:
    """
    Find the position of the new iterators terminal tag with the same value.
    :param tokens: a list of page tokens.
    :param start_position: first possible tag position.
    :return: tag position if found, None otherwise.
    """
    i = start_position
    while i < len(tokens):
        if tokens[i].token_type == TOKEN_TYPE.CLOSING_TAG and tokens[i].value == tokens[start_position].value:
            return i
        i += 1

    return None


def find_iterator_start(tokens: [Token], start_position: int) -> int | None:
    """
    Find the position of the previous iterator start tag with the same value.
    :param tokens: a list of page tokens.
    :param start_position: first possible tag position.
    :return: tag position if found, None otherwise.
    """
    i = start_position
    while i > 0:
        if tokens[i].token_type == TOKEN_TYPE.OPENING_TAG and tokens[i].value == tokens[start_position].value:
            return i
        i -= 1

    return None


def wrapper_generalization_iterator(wrapper: [Token], tag_mismatch: str, internal_wrapper: [Token]) -> [Token]:
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
        while i > 0 and wrapper[i].token_type == TOKEN_TYPE.OPTIONAL:
            i -= 1

        # Find the previous terminal tag of the same type.
        if wrapper[i].token_type == TOKEN_TYPE.CLOSING_TAG and wrapper[i].value == tag_mismatch:
            # Previous terminal tag found.
            while i > 0:
                # Find the start tag.
                if wrapper[i].token_type == TOKEN_TYPE.OPENING_TAG and wrapper[i].value == tag_mismatch:
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
    new_iterator = Token(token_type=TOKEN_TYPE.ITERATOR, value=internal_wrapper)
    wrapper.append(new_iterator)
    return wrapper


def wrapper_generalization_optional_field(wrapper: [Token], token: Token) -> [Token]:
    """
    Generalize the wrapper by incorporating optional fields.
    :param wrapper: currently generated wrapper.
    :param token: page token.
    :return: generalized wrapper.
    """
    wrapper.append(Token(token_type=TOKEN_TYPE.OPTIONAL, value=" ".join(["<", token.value, "/>"])))
    return wrapper


def find_iterator(previous_token: Token, page_token: Token, page: [Token], index: int, wrapper: [Token]) -> [Token]:
    """
    Tries to find an iterator on the page.
    :param previous_token: Token before the current token.
    :param page_token: current page token.
    :param page: current page.
    :param index: current page index.
    :param wrapper: currently generated wrapper
    :return:
    """
    if previous_token.token_type == TOKEN_TYPE.CLOSING_TAG and page_token.token_type == TOKEN_TYPE.OPENING_TAG \
            and previous_token.value == page_token.value:
        # possible iterator discovered on the page.
        # Verify with square matching.
        # confirm existence of equal terminal tag.
        new_iterator_end = find_new_iterator_end(tokens=page, start_position=index)

        if new_iterator_end is None:
            return None
        previous_iterator_start = find_iterator_start(tokens=page,
                                                      start_position=index - 1)

        if previous_iterator_start is None:
            return None
        previous_square = page[previous_iterator_start:index]
        square = page[index:new_iterator_end + 1]
        internal_wrapper = road_runner(first_page=previous_square,
                                       second_page=square,
                                       first_index=0,
                                       second_index=0,
                                       wrapper=[])

        if internal_wrapper is not None:
            return wrapper_generalization_iterator(wrapper=wrapper,
                                                   tag_mismatch=page_token.value,
                                                   internal_wrapper=internal_wrapper), new_iterator_end
    return None


def road_runner(first_page: [Token], second_page: [Token], first_index: int, second_index: int, wrapper: [Token]) \
        -> [Token]:
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
    if first_index == len(first_page) and second_index == len(second_page) \
            or first_index >= len(first_page) or second_index >= len(second_page):
        # The algorithm is finished.
        return wrapper

    page1_token = first_page[first_index]
    page2_token = second_page[second_index]

    # Check if tokens are equal.
    if compare_tokens(page1_token, page2_token):
        # Tokens are equal on both pages, add the token to the wrapper and go deeper.
        wrapper.append(page1_token)
        return road_runner(first_page=first_page,
                           second_page=second_page,
                           first_index=first_index + 1,
                           second_index=second_index + 1,
                           wrapper=wrapper)
    else:
        # Tokens aren't equal on both pages.
        # Check whether both tokens are database fields.
        if page1_token.token_type == TOKEN_TYPE.DATABASE_FIELD and page2_token.token_type == TOKEN_TYPE.DATABASE_FIELD:
            # Both tokens are database fields, so it's a string mismatch.
            wrapper.append(Token(token_type=TOKEN_TYPE.DATABASE_FIELD, value=STRING_MISMATCH_FIELD))
            return road_runner(first_page, second_page, first_index + 1, second_index + 1, wrapper)

        # At least one of the tokens isn't a database field, so it's a tag mismatch.
        # check for iterators -> square location by terminal–tag search

        # Get previous tokens.
        previous_page1_token = first_page[first_index - 1]
        previous_page2_token = second_page[second_index - 1]

        # Check if the previous token on the first page is a terminal tag and
        # matches the current token on the first page.
        found_iterator = find_iterator(wrapper=wrapper,
                                       previous_token=previous_page1_token,
                                       page_token=page1_token,
                                       page=first_page,
                                       index=first_index)

        if found_iterator is not None:
            new_wrapper, previous_terminal_position = found_iterator
            return road_runner(first_page=first_page,
                               second_page=second_page,
                               first_index=previous_terminal_position + 1,
                               second_index=second_index,
                               wrapper=new_wrapper)

        # Check if the previous token on the second page is a terminal tag and
        # matches the current token on the second page.
        found_iterator = find_iterator(wrapper=wrapper,
                                       previous_token=previous_page2_token,
                                       page_token=page2_token,
                                       page=second_page,
                                       index=second_index)

        if found_iterator is not None:
            new_wrapper, previous_terminal_position = found_iterator
            return road_runner(first_page=first_page,
                               second_page=second_page,
                               first_index=first_index,
                               second_index=previous_terminal_position + 1,
                               wrapper=new_wrapper)

        # Iterator wasn't found, check for optionals.
        # Optional pattern location by cross–search.

        # Try longer optional searches.
        for i in range(1, max(len(first_page) - first_index, len(second_page) - second_index)):
            # Check whether the first page contains an optional pattern.
            if first_index + i < len(first_page) and compare_tokens(first_page[first_index + i], page2_token):
                # Skipping an optional pattern worked, generalize wrapper and proceed.
                wrapper = wrapper_generalization_optional_field(wrapper=wrapper, token=page1_token)
                return road_runner(first_page, second_page, first_index + 1, second_index, wrapper)

            # Check whether the second page contains an optional pattern.
            elif second_index + i < len(second_page) and compare_tokens(page1_token, second_page[second_index + i]):
                # Skipping an optional pattern worked, generalize wrapper and proceed.
                wrapper = wrapper_generalization_optional_field(wrapper=wrapper, token=page2_token)
                return road_runner(first_page, second_page, first_index, second_index + 1, wrapper)
        else:
            # Backtrace -> End of the branch.
            return []
            # #Try skipping the first token
            # new_wrapper = road_runner(first_page, second_page, first_index + 1, second_index, wrapper)
            # if len(new_wrapper) != 0:
            #     return new_wrapper
            # #Try skipping the second token
            # new_wrapper = road_runner(first_page, second_page, first_index, second_index + 1, wrapper)
            # if len(new_wrapper) != 0:
            #     return new_wrapper
            # print("Error skipping optional pattern.", file=sys.stderr)
            # return road_runner(first_page, second_page, first_index + 1, second_index + 1, wrapper)



def start_running(first_html: str, second_html: str) -> None:
    """
    Runs the roadrunner algorithm on the provided pages.
    :param first_html: HTML of the first page.
    :param second_html: HTML of the second page.
    """
    sys.setrecursionlimit(5000)
    first_page, second_page = prepare_data(first_html=first_html, second_html=second_html)
    wrapper = road_runner(first_page, second_page, 0, 0, [])
    solution = get_printable_wrapper(wrapper=wrapper)
    print(solution)
