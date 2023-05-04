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
    Compare two token and returns True if they're equal and False otherwise.
    :param first: first token to be compared.
    :param second: second token to be compared.
    :return: True if the tokens are equal and False otherwise.
    """
    if first[0] == second[0] and first[1] == second[1]:
        return True
    elif first[0] == "optional" and first[1][1:-2] == second[1]:
        print("OPTIONAL MATCHING - MIGHT REQUIRE ADDITIONAL ATTENTION")
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


def roadrunner(wrapper: [str], sample: [str], wrapper_index: int, sample_index: int, solution: [str]) -> [str]:
    """
    Runs the roadrunner algorithm on the provided pages.
    :param wrapper: first html page.
    :param sample: second html page.
    :param wrapper_index: current pointer index on the first page.
    :param sample_index: current pointer index on the second page.
    :param solution: current generated solution wrapper.
    :return: generated wrapper.
    """
    # Recursive end condition.
    if wrapper_index == len(wrapper) and sample_index == len(sample):
        # The algorithm is finished.
        return solution

    wrapper_token = wrapper[wrapper_index]
    sample_token = sample[sample_index]

    # IF MATCHING TOKENS, SIMPLY APPEND TO THE WRAPPER
    if compare_tokens(wrapper_token, sample_token):
        solution.append(wrapper_token)
        return roadrunner(wrapper, sample, wrapper_index + 1, sample_index + 1, solution)
    else:
        # handle string mismatch:
        if wrapper_token[0] == "data" and sample_token[0] == "data":
            solution.append(["data", "#PCDATA"])
            return roadrunner(wrapper, sample, wrapper_index + 1, sample_index + 1, solution)
        # tag mismatch - either an optional or an iterative
        else:
            iterative = True

            # check for iterative
            prev_wrap_token = wrapper[wrapper_index - 1]
            prev_smpl_token = sample[sample_index - 1]

            # iterator discovered on wrapper side
            if prev_wrap_token[0] == "tail_tag" and wrapper_token[0] == "head_tag" and prev_wrap_token[1] == \
                    wrapper_token[1]:
                # confirm existance of equal terminal tag
                iter_found, iter_end_indx = find_iterator_end(wrapper, wrapper_index)

                if iter_found:

                    prev_iter_found, prev_iter_start_indx = find_prev_iterator_start(wrapper, wrapper_index - 1)

                    if prev_iter_found:

                        prev_square = wrapper[prev_iter_start_indx:wrapper_index]
                        square = wrapper[wrapper_index:iter_end_indx + 1]

                        internal_wrapper = roadrunner(prev_square, square, 0, 0, [])

                        if internal_wrapper is not None:
                            new_wrapper = clean_wrapper_iterators(solution, wrapper_token[1], internal_wrapper)
                            return roadrunner(wrapper, sample, wrapper_index, iter_end_indx + 1, new_wrapper)

                        else:
                            iterative = False
                    else:
                        iterative = False

                else:
                    iterative = False

            # iterator discovered on sample side
            elif prev_smpl_token[0] == "tail_tag" and sample_token[0] == "head_tag" and prev_smpl_token[1] == \
                    sample_token[1]:
                # confirm existance of equal terminal tag
                iter_found, iter_end_indx = find_iterator_end(sample, sample_index)

                if iter_found:

                    prev_iter_found, prev_iter_start_indx = find_prev_iterator_start(sample, sample_index - 1)

                    if prev_iter_found:

                        prev_square = sample[prev_iter_start_indx:sample_index]
                        square = sample[sample_index:iter_end_indx + 1]

                        internal_wrapper = roadrunner(prev_square, square, 0, 0, [])

                        if internal_wrapper is not None:
                            solution = clean_wrapper_iterators(solution, sample_token[1], internal_wrapper)
                            return roadrunner(wrapper, sample, wrapper_index, iter_end_indx + 1, solution)

                        else:
                            iterative = False

                    else:
                        iterative = False

                else:
                    iterative = False
            else:
                iterative = False

            # check for optional
            if not iterative:
                # option is present on wrapper
                if compare_tokens(wrapper[wrapper_index + 1], sample_token):
                    optional = ["optional", " ".join(["(", wrapper_token[1], ")?"])]
                    solution.append(optional)
                    return roadrunner(wrapper, sample, wrapper_index + 1, sample_index, solution)

                elif compare_tokens(wrapper_token, sample[sample_index + 1]):
                    optional = ["optional", " ".join(["(", sample_token[1], ")?"])]
                    solution.append(optional)
                    return roadrunner(wrapper, sample, wrapper_index, sample_index + 1, solution)
                else:
                    # print(": >>>> ", wrapper_token, " vs ", sample_token)
                    # print(": >>>> ", wrapper_tokens[indx_w+1], " vs ", sample_token)
                    # print(": >>>> ", wrapper_token, " vs ", sample_tokens[indx_s+1])
                    # print("ERROR MATCHING OPTIONAL !!! ")
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
