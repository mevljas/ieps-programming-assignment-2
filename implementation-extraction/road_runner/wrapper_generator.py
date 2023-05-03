from road_runner.helpers.constants import STRING_MISMATCH_FIELD, OPTIONAL_FIELD, ITERATOR_FIELD, HTML_TAG_START


def get_tag_sublist(tokens: [str], index: int) -> [str]:
    """
    Gets a sublist of tokens from the opening to the closing tag.
    :param tokens: list of tokens.
    :param index: index of the tag.
    :return: A sublist of tokens from the opening to the closing tag.
    """
    start_index = index
    required_tail_tags = 0
    tokens_subset = []
    while index < len(tokens):
        if required_tail_tags == 0 and index != start_index:
            break
        tokens_subset.append(tokens[index])
        current_tag = tokens[index]
        if current_tag[0] == "<":
            if current_tag[1] != "/":
                required_tail_tags += 1
            else:
                required_tail_tags -= 1
        index += 1
    return tokens_subset


def count_occurrences(wrapper_parts: [str], part_index: int) -> int:
    """
    Counts occurrences of the part at the index part_index from the part_index to the end of the wrapper_parts list.
    :param wrapper_parts: list of road_runner parts.
    :param part_index: index of the searched part.
    :return:
    """
    current_part = wrapper_parts[part_index]
    parts_count = 0
    while part_index < len(wrapper_parts) and wrapper_parts[part_index] == current_part:
        parts_count += 1
        part_index += 1
    return parts_count


def find_first_match(first_page: [str], second_page: [str], first_page_index: int,
                     second_page_index: int) -> ([str], int, int):
    """
    Finds the first match between token groups of both pages.
    :param first_page: first page tokens.
    :param second_page: second page tokens.
    :param first_page_index: index of the first page token.
    :param second_page_index: index. of the second page token.
    :return: road_runner, first page index and second page index.
    """
    while first_page_index < len(first_page):
        while second_page_index < len(second_page):
            wrapper = generate_wrapper(first_page[first_page_index],
                                       second_page[second_page_index])
            if len(wrapper) != 0:
                return wrapper, first_page_index, second_page_index
            second_page_index += 1
        first_page_index += 1
    return None


def generate_wrapper(wrapper: [str], sample: [str]) -> [str]:
    """
    Generates the road_runner from the tokens of both pages.
    :param wrapper: a list of first page's tokens.
    :param sample: a list of second page's tokens
    :return: a road_runner list.
    """
    wrapper_index = 0
    sample_index = 0
    solution = []

    if len(wrapper) == len(sample):
        # Pages are both equally long.
        while wrapper_index < len(wrapper) and sample_index < len(sample):
            if wrapper[wrapper_index] == sample[sample_index]:
                # Tokens are the same on both pages. Add it to the solution.
                solution.append(wrapper[wrapper_index])
            else:
                # Tokens differ.
                if wrapper[wrapper_index][0] != HTML_TAG_START:
                    # Token is not an opening tag.
                    # STRING MISMATCH
                    solution.append(STRING_MISMATCH_FIELD)
                else:
                    # Tokens are completely different.
                    return ""
            wrapper_index += 1
            sample_index += 1
    else:
        # Pages are not equally long.
        # TAG MISMATCHES
        wrapper_parts = []
        first_page_token_groups = []
        second_page_token_groups = []
        wrapper_index = 1
        sample_index = 1
        # Group together tokens inside top level tags.
        while wrapper_index < len(wrapper) - 1:
            first_page_tag_group = get_tag_sublist(tokens=wrapper, index=wrapper_index)
            wrapper_index += len(first_page_tag_group)
            first_page_token_groups.append(first_page_tag_group)
        while sample_index < len(sample) - 1:
            second_page_tag_group = get_tag_sublist(tokens=sample, index=sample_index)
            sample_index += len(second_page_tag_group)
            second_page_token_groups.append(second_page_tag_group)
        first_page_group_index = 0
        second_page_group_index = 0
        while first_page_group_index < len(first_page_token_groups) \
                and second_page_group_index < len(second_page_token_groups):
            # Concatenate together opening and closing tags.
            wrapper_part = generate_wrapper(wrapper=first_page_token_groups[first_page_group_index],
                                            sample=second_page_token_groups[second_page_group_index])
            if len(wrapper_part) != 0:
                # Save road_runner part.
                wrapper_parts.append(wrapper_part)
                first_page_group_index += 1
                second_page_group_index += 1
            else:
                # Find partial match?
                first_match = find_first_match(
                    first_page=first_page_token_groups,
                    second_page=second_page_token_groups,
                    first_page_index=first_page_group_index + 1,
                    second_page_index=second_page_group_index + 1)
                if first_match:
                    wrapper_part, wrapper_index, sample_index = first_match
                    while first_page_group_index != wrapper_index:
                        wrapper_parts.append("(")
                        wrapper_parts.append("".join(first_page_token_groups[first_page_group_index]))
                        wrapper_parts.append(OPTIONAL_FIELD)
                        first_page_group_index += 1
                    while second_page_group_index != sample_index:
                        wrapper_parts.append("(")
                        wrapper_parts.append("".join(second_page_token_groups[second_page_group_index]))
                        wrapper_parts.append(OPTIONAL_FIELD)
                        second_page_group_index += 1
                    wrapper_parts.append(wrapper_part)
                    first_page_group_index += 1
                    second_page_group_index += 1
                else:
                    if len(first_page_token_groups) == len(second_page_token_groups) and len(
                            first_page_token_groups) == 1:
                        # Both groups contain only one element.
                        while len(first_page_token_groups[0]) != len(second_page_token_groups[0]):
                            # While first items of both token groups are of a different length.
                            if len(first_page_token_groups[0]) > len(second_page_token_groups[0]):
                                # Remove the first tag
                                tag_sublist = get_tag_sublist(tokens=first_page_token_groups[0], index=1)
                                first_page_token_groups[0] = list(tag_sublist)
                            else:
                                # Remove the first tag
                                tag_sublist = get_tag_sublist(tokens=second_page_token_groups[0], index=1)
                                second_page_token_groups[0] = list(tag_sublist)
                        wrapper_part = generate_wrapper(wrapper=first_page_token_groups[0],
                                                        sample=second_page_token_groups[0])
                        if len(wrapper_part) == 0:
                            break
                        else:
                            wrapper_parts.append(wrapper_part)
                    else:
                        break
                    first_page_group_index += 1
                    second_page_group_index += 1
        wrapper_part_counter = 0
        while wrapper_part_counter < len(wrapper_parts):
            wrapper_index = count_occurrences(wrapper_parts=wrapper_parts, part_index=wrapper_part_counter)
            if wrapper_index > 1:
                # ITERATOR
                solution.append("(")
                solution.append(wrapper_parts[wrapper_part_counter])
                solution.append(ITERATOR_FIELD)
            else:
                solution.append(wrapper_parts[wrapper_part_counter])
            wrapper_part_counter += wrapper_index
    return solution
