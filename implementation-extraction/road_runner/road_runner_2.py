import sys

from road_runner.helpers.CustomHTMLParser import CustomHTMLParser
from road_runner.helpers.data_processor import parse_html


def get_iterator_string(iterator):
    str_iter = "( "

    for token in iterator:
        if token[0] == "head_tag":
            str_iter += "".join(["<", token[1], ">"])
        elif token[0] == "tail_tag":
            str_iter += "".join(["</", token[1], ">"])
        elif token[0] == "optional":
            str_iter += token[1] + ""
        else:
            str_iter += token[1]

    str_iter += " )+\n"

    return str_iter


def get_optional_string(optional):
    str_opt = "( "

    for token in optional:
        if token[0] == "head_tag":
            str_opt += "".join(["<", token[1], ">"])
        elif token[0] == "tail_tag":
            str_opt += "".join(["</", token[1], ">"])
        elif token[0] == "optional":
            str_opt += token[1] + ""
        else:
            str_opt += token[1]

    str_opt += " )?\n"

    return str_opt


def write_final_wrapper_as_ufre(wrapper):
    ufre = ""

    for token in wrapper:
        if token[0] == "head_tag":
            ufre += "".join(["<", token[1], ">\n"])
        elif token[0] == "tail_tag":
            ufre += "".join(["</", token[1], ">\n"])
        elif token[0] == "optional":
            ufre += token[1] + "\n"
        elif token[0] == "iterator":
            ufre += get_iterator_string(token[1])
        else:
            ufre += token[1] + "\n"

    return ufre


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


def find_iterator_end(tokens, start_indx):
    end_tag_found = False
    i = start_indx

    while i < len(tokens):

        if tokens[i][0] == "tail_tag" and tokens[i][1] == tokens[start_indx][1]:
            end_tag_found = True
            break

        i += 1

    return end_tag_found, i


def find_prev_iterator_start(tokens, start_indx):
    start_tag_found = False
    i = start_indx

    while i > 0:

        if tokens[i][0] == "head_tag" and tokens[i][1] == tokens[start_indx][1]:
            start_tag_found = True
            break

        i -= 1

    return start_tag_found, i


def find_end_of_optional(tokens, start_indx, tag):
    i = start_indx
    found = False

    while i < len(tokens) - 1:

        if tokens[i][0] == "tail_tag" and tokens[i][1] == tag:
            found = True
            break

        i += 1

    return found, i


def clean_wrapper_iterators(wrapper, iterator_tag, internal_wrapper):
    i = len(wrapper) - 1

    new_end = None

    while i > 0:

        while i > 0 and wrapper[i][0] == "optional":
            i -= 1

        if wrapper[i][0] == "tail_tag" and wrapper[i][1] == iterator_tag:

            while i > 0:

                if wrapper[i][0] == "head_tag" and wrapper[i][1] == iterator_tag:
                    new_end = i
                    i -= 1
                    break
                i -= 1
        else:
            break

    if new_end is None:
        return wrapper

    # we found new wrapper
    wrapper = wrapper[:new_end]
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
    wrapper.append(["optional", " ".join(["(", token[1], ")?"])])
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
            # check for iterator

            # Get previous tokens.
            previous_page1_token = first_page[first_index - 1]
            previous_page2_token = second_page[second_index - 1]

            if previous_page1_token[0] == "tail_tag" \
                    and page1_token[0] == "head_tag" \
                    and previous_page1_token[1] == page1_token[1]:
                # iterator discovered on wrapper side
                # confirm existance of equal terminal tag
                iter_found, iter_end_indx = find_iterator_end(first_page, first_index)

                if iter_found:

                    prev_iter_found, prev_iter_start_indx = find_prev_iterator_start(first_page, first_index - 1)

                    if prev_iter_found:

                        prev_square = first_page[prev_iter_start_indx:first_index]
                        square = first_page[first_index:iter_end_indx + 1]

                        internal_wrapper = roadrunner(prev_square, square, 0, 0, [])

                        if internal_wrapper is not None:
                            new_wrapper = clean_wrapper_iterators(wrapper, page1_token[1], internal_wrapper)
                            return roadrunner(first_page, second_page, first_index, iter_end_indx + 1, new_wrapper)

                        else:
                            iterative = False
                    else:
                        iterative = False

                else:
                    iterative = False

            # iterator discovered on sample side
            elif previous_page2_token[0] == "tail_tag" and page2_token[0] == "head_tag" and previous_page2_token[1] == \
                    page2_token[1]:
                # confirm existance of equal terminal tag
                iter_found, iter_end_indx = find_iterator_end(second_page, second_index)

                if iter_found:

                    prev_iter_found, prev_iter_start_indx = find_prev_iterator_start(second_page, second_index - 1)

                    if prev_iter_found:

                        prev_square = second_page[prev_iter_start_indx:second_index]
                        square = second_page[second_index:iter_end_indx + 1]

                        internal_wrapper = roadrunner(prev_square, square, 0, 0, [])

                        if internal_wrapper is not None:
                            wrapper = clean_wrapper_iterators(wrapper, page2_token[1], internal_wrapper)
                            return roadrunner(first_page, second_page, first_index, iter_end_indx + 1, wrapper)

                        else:
                            iterative = False

                    else:
                        iterative = False

                else:
                    iterative = False
            else:
                iterative = False

            # Check for optionals.
            if not iterative:
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
    ufre = write_final_wrapper_as_ufre(wrapper)
    print(ufre)
