from bs4 import BeautifulSoup


def generate_html_tags(html_element: any) -> [str]:
    """
    Generate HTML tags (tokens) from BeautifulSoup HTML elements.
    :param html_element: BeautifulSoup element
    :return: a list of HTML tags.
    """
    yield f'<{html_element.name}>'
    for child in html_element.contents:
        if not isinstance(child, str):
            yield from generate_html_tags(html_element=child)
        else:
            yield from child.split()
    yield f'</{html_element.name}>'


def group_elements(tokens: [str]) -> [str]:
    """
    Group elements between starting and closing tags together.
    :param tokens: a list of filtered tokens.
    :return: a list of grouped filtered tokens.
    """
    final_elements = []
    window_start = 0
    while window_start < len(tokens):
        if tokens[window_start][0] != "<":
            # Token is a data element or a closing tag.
            window_end = window_start
            while tokens[window_end][0] != "<":
                # While the current token is not the closing tag.
                window_end = window_end + 1
            # The matching tail tag was found.
            # Concatenate all items between the opening and closing tags.
            final_elements.append(" ".join(tokens[window_start:window_end]))
            window_start = window_end
        else:
            # Append the opening tag.
            final_elements.append(tokens[window_start])
            window_start = window_start + 1
    return final_elements


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
    :param wrapper_parts: list of wrapper parts.
    :param part_index: index of the searched part.
    :return:
    """
    current_part = wrapper_parts[part_index]
    parts_count = 0
    while part_index < len(wrapper_parts) and wrapper_parts[part_index] == current_part:
        parts_count += 1
        part_index += 1
    return parts_count


def find_first_match(first_page_token_groups: [str], second_page_token_groups: [str], first_page_counter: int,
                     second_page_counter: int) -> ([str], int, int):
    """
    Finds the first match between token groups of both pages.
    :param first_page_token_groups: first page tokens.
    :param second_page_token_groups: second page tokens.
    :param first_page_counter: index of the first page token.
    :param second_page_counter: index. of the second page token.
    :return: wrapper, first page counter and second page counter.
    """
    while first_page_counter < len(first_page_token_groups):
        while second_page_counter < len(second_page_token_groups):
            wrapper = generate_wrapper(first_page_token_groups[first_page_counter],
                                       second_page_token_groups[second_page_counter])
            if len(wrapper) != 0:
                return wrapper, first_page_counter, second_page_counter
            second_page_counter += 1
        first_page_counter += 1
    return None


def generate_wrapper(first_page_tokens: [str], second_page_tokens: [str]) -> [str]:
    """
    Generates the wrapper from the tokens of both pages.
    :param first_page_tokens: a list of first page's tokens.
    :param second_page_tokens: a list of second page's tokens
    :return: a wrapper list.
    """
    first_page_token_counter = 0
    second_page_token_counter = 0
    wrapper = []

    if len(first_page_tokens) == len(second_page_tokens):
        while first_page_token_counter < len(first_page_tokens) and second_page_token_counter < len(second_page_tokens):
            if first_page_tokens[first_page_token_counter] == second_page_tokens[second_page_token_counter]:
                wrapper.append(first_page_tokens[first_page_token_counter])
            else:
                if first_page_tokens[first_page_token_counter][0] != "<":
                    wrapper.append("#PCDATA")
                else:
                    return ""
            first_page_token_counter += 1
            second_page_token_counter += 1
    else:
        wrapper_parts = []
        first_page_token_groups = []
        second_page_token_groups = []
        first_page_token_counter = 1
        second_page_token_counter = 1
        while first_page_token_counter < len(first_page_tokens) - 1:
            tag1_sublist = get_tag_sublist(tokens=first_page_tokens, index=first_page_token_counter)
            first_page_token_counter += len(tag1_sublist)
            first_page_token_groups.append(tag1_sublist)
        while second_page_token_counter < len(second_page_tokens) - 1:
            tag2_sublist = get_tag_sublist(tokens=second_page_tokens, index=second_page_token_counter)
            second_page_token_counter += len(tag2_sublist)
            second_page_token_groups.append(tag2_sublist)
        tag1_sublist_counter = 0
        tag2_sublist_counter = 0
        while tag1_sublist_counter < len(first_page_token_groups) and tag2_sublist_counter < len(
                second_page_token_groups):
            wrapper_part = generate_wrapper(first_page_token_groups[tag1_sublist_counter],
                                            second_page_token_groups[tag2_sublist_counter])
            if len(wrapper_part) != 0:
                wrapper_parts.append(wrapper_part)
                tag1_sublist_counter += 1
                tag2_sublist_counter += 1
            else:
                first_match = find_first_match(
                    first_page_token_groups=first_page_token_groups,
                    second_page_token_groups=second_page_token_groups,
                    first_page_counter=tag1_sublist_counter + 1,
                    second_page_counter=tag2_sublist_counter + 1)
                if first_match:
                    wrapper_part, first_page_counter, second_page_counter = first_match
                    while tag1_sublist_counter != first_page_counter:
                        wrapper_parts.append("(")
                        wrapper_parts.append("".join(first_page_token_groups[tag1_sublist_counter]))
                        wrapper_parts.append(")?")
                        tag1_sublist_counter += 1
                    while tag2_sublist_counter != second_page_counter:
                        wrapper_parts.append("(")
                        wrapper_parts.append("".join(second_page_token_groups[tag2_sublist_counter]))
                        wrapper_parts.append(")?")
                        tag2_sublist_counter += 1
                    wrapper_parts.append(wrapper_part)
                    tag1_sublist_counter += 1
                    tag2_sublist_counter += 1
                else:
                    if len(first_page_token_groups) == len(second_page_token_groups) and len(
                            first_page_token_groups) == 1:
                        while len(first_page_token_groups[0]) != len(second_page_token_groups[0]):
                            if len(first_page_token_groups[0]) > len(second_page_token_groups[0]):
                                r1 = get_tag_sublist(tokens=first_page_token_groups[0], index=1)
                                first_page_token_groups[0] = list(r1)
                            else:
                                r1 = get_tag_sublist(tokens=second_page_token_groups[0], index=1)
                                second_page_token_groups[0] = list(r1)
                        wrapper_part = generate_wrapper(first_page_token_groups[0], second_page_token_groups[0])
                        if len(wrapper_part) == 0:
                            break
                        else:
                            wrapper_parts.append(wrapper_part)
                    else:
                        break
                    tag1_sublist_counter += 1
                    tag2_sublist_counter += 1
        wrapper_part_counter = 0
        while wrapper_part_counter < len(wrapper_parts):
            first_page_counter = count_occurrences(wrapper_parts=wrapper_parts, part_index=wrapper_part_counter)
            if first_page_counter > 1:
                wrapper.append("(")
                wrapper.append(wrapper_parts[wrapper_part_counter])
                wrapper.append(")+")
            else:
                wrapper.append(wrapper_parts[wrapper_part_counter])
            wrapper_part_counter += first_page_counter
    return "\n".join(wrapper)


def clean_html_soup(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Removes all script and style tags from the html.
    :param soup: BeautifulSoup object with html data to be cleaned.
    :return: BeautifulSoup object with cleaned html data.
    """
    [x.extract() for x in soup.findAll(['script', 'style'])]
    return soup


def create_html_soup(html: str) -> BeautifulSoup:
    """
    Generate BeautifulSoup object with the provided html.
    :param html: html data to be used.
    :return: Generated BeautifulSoup object.
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup


def filter_tokens(tokens: [str]) -> [str]:
    """
    Filter a list of tokens and removes unnecessary ones.
    :param tokens: a list of tokens.
    :return: filtered list of tokens.
    """
    return list(filter(lambda token: token not in ["<br>", "</br>", "<strong>", "</strong>", "<em>"], tokens))


def run_road_runner(first_html: str, second_html: str) -> None:
    # Generate Beautiful soup objects.
    first_soup = create_html_soup(html=first_html)
    second_soup = create_html_soup(html=second_html)

    # Remove all style and script tags from the html.
    first_soup_cleaned = clean_html_soup(soup=first_soup)
    second_soup_cleaned = clean_html_soup(soup=second_soup)

    # Tokenize.
    first_page_tokens = list(generate_html_tags(html_element=first_soup_cleaned.body))
    second_page_tokens = list(generate_html_tags(html_element=second_soup_cleaned.body))

    # Filter tokens.
    first_page_tokens_filtered = filter_tokens(tokens=first_page_tokens)
    second_page_tokens_filtered = filter_tokens(tokens=second_page_tokens)

    # Concatenate multiple elements between tags.
    first_page_tokens_concatenated = group_elements(tokens=first_page_tokens_filtered)
    second_page_tokens_concatenated = group_elements(tokens=second_page_tokens_filtered)

    # Generate wrapper.
    wrapper = generate_wrapper(first_page_tokens=first_page_tokens_concatenated,
                               second_page_tokens=second_page_tokens_concatenated)
    print(wrapper)
