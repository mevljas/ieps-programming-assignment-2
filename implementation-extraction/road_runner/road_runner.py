from road_runner.helpers.data_processor import prepare_data
from road_runner.wrapper_generator import generate_wrapper


def road_runner(first_html: str, second_html: str) -> None:
    """
    Runs the roadrunner algorithm on the provided pages.
    :param first_html: HTML of the first page.
    :param second_html: HTML of the second page.
    """
    first_page, second_page = prepare_data(first_html=first_html, second_html=second_html)
    wrapper = generate_wrapper(wrapper=first_page, sample=second_page)
    print(wrapper)
