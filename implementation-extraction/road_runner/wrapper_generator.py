from road_runner.helpers.constants import STRING_MISMATCH_FIELD, OPTIONAL_FIELD, ITERATOR_FIELD, HTML_TAG_START


def remove_token_parents(tokens: [str], position: int) -> [str]:
    """
    Gets a subgroup of tokens from the opening tag at index to the closing tag.
    :param tokens: list of tokens.
    :param position: index of the removing tag.
    :return: a subgroup of tokens from the opening tag at index to the closing tag.
    """
    start_position = position
    required_tail_tags = 0
    tokens_subset = []
    while position < len(tokens):
        if required_tail_tags == 0 and position != start_position:
            break
        tokens_subset.append(tokens[position])
        current_tag = tokens[position]
        if current_tag[0] == "<":
            if current_tag[1] != "/":
                required_tail_tags += 1
            else:
                required_tail_tags -= 1
        position += 1
    return tokens_subset


def wrapper_generalization_optional_field(solution: [str], tokens_index: int, length: int, tokens: [str]) \
        -> ([str], int):
    """
    Generalize the wrapper by incorporating optional fields.
    :param solution: currently generated wrapper.
    :param tokens_index: current token index.
    :param length: maximum allowed length.
    :param tokens: page tokens.
    :return: generalized solution and latest tokens index.
    """
    while tokens_index != length:
        solution.extend(["(", "".join(tokens[tokens_index]), OPTIONAL_FIELD])
        tokens_index += 1
    return solution, tokens_index + 1


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


def find_optional_field(first_page: [str], second_page: [str], first_page_index: int,
                        second_page_index: int) -> ([str], int, int):
    """
    Finds minimal optional field between two pages (token groups).
    Optional Pattern Location by Cross–Search.
    :param first_page: first page tokens.
    :param second_page: second page tokens.
    :param first_page_index: index of the first page token.
    :param second_page_index: index of the second page token.
    :return: wrapper, first page index and second page index.
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
        solution_parts = []
        wrapper_token_groups = []
        sample_token_groups = []
        wrapper_index = 1
        sample_index = 1
        # Group together tokens inside top level tags.
        while wrapper_index < len(wrapper) - 1:
            first_page_tag_group = remove_token_parents(tokens=wrapper, position=wrapper_index)
            wrapper_index += len(first_page_tag_group)
            wrapper_token_groups.append(first_page_tag_group)
        while sample_index < len(sample) - 1:
            second_page_tag_group = remove_token_parents(tokens=sample, position=sample_index)
            sample_index += len(second_page_tag_group)
            sample_token_groups.append(second_page_tag_group)
        wrapper_group_index = 0
        sample_group_index = 0
        while wrapper_group_index < len(wrapper_token_groups) \
                and sample_group_index < len(sample_token_groups):
            # Concatenate together opening and closing tags.
            partial_solution = generate_wrapper(wrapper=wrapper_token_groups[wrapper_group_index],
                                                sample=sample_token_groups[sample_group_index])
            if len(partial_solution) != 0:
                # Save a part of the wrapper.
                solution_parts.append(partial_solution)
                wrapper_group_index += 1
                sample_group_index += 1
            else:
                # Find optional field.
                optional_field = find_optional_field(
                    first_page=wrapper_token_groups,
                    second_page=sample_token_groups,
                    first_page_index=wrapper_group_index + 1,
                    second_page_index=sample_group_index + 1)
                if optional_field:
                    # Tag Mismatches: Discovering Optionals -> Wrapper Generalization
                    partial_solution, wrapper_index, sample_index = optional_field
                    # Add optional fields to the solution.
                    solution_parts, wrapper_group_index = wrapper_generalization_optional_field(
                        solution=solution_parts,
                        tokens_index=wrapper_group_index,
                        length=wrapper_index,
                        tokens=wrapper_token_groups)
                    solution_parts, sample_group_index = wrapper_generalization_optional_field(
                        solution=solution_parts,
                        tokens_index=sample_group_index,
                        length=sample_index,
                        tokens=sample_token_groups)
                    solution_parts.append(partial_solution)
                else:
                    if len(wrapper_token_groups) == len(sample_token_groups) and len(
                            wrapper_token_groups) == 1:
                        # Both groups contain only one token group.
                        while len(wrapper_token_groups[0]) != len(sample_token_groups[0]):
                            # While items of both token groups are of a different length.
                            # Remove the top level token (top level opening and closing tag) of the longer group.
                            if len(wrapper_token_groups[0]) > len(sample_token_groups[0]):
                                wrapper_token_groups[0] = remove_token_parents(tokens=wrapper_token_groups[0],
                                                                               position=1)
                            else:
                                sample_token_groups[0] = remove_token_parents(tokens=sample_token_groups[0],
                                                                              position=1)
                        partial_solution = generate_wrapper(wrapper=wrapper_token_groups[0],
                                                            sample=sample_token_groups[0])
                        if len(partial_solution) == 0:
                            break
                        else:
                            solution_parts.append(partial_solution)
                    else:
                        break
                    wrapper_group_index += 1
                    sample_group_index += 1
        wrapper_part_counter = 0
        while wrapper_part_counter < len(solution_parts):
            wrapper_index = count_occurrences(wrapper_parts=solution_parts, part_index=wrapper_part_counter)
            if wrapper_index > 1:
                # ITERATOR
                solution.extend(["(", solution_parts[wrapper_part_counter], ITERATOR_FIELD])
            else:
                solution.append(solution_parts[wrapper_part_counter])
            wrapper_part_counter += wrapper_index
    return solution
