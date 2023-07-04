from dff.utils.testing import check_happy_path
from examples import generic_responses as test

# testing
HAPPY_PATH = [
    ("Hi", "Hi, how are you?"),  # start_node -> node1
    ("I'm fine, square root of two times square root of three is square root of six is it?", "Yes"),  # node1 -> generic_response
    ("Ok", "Ooops"),  # generic_response -> fallback_node
]


if __name__ == "__main__":
    check_happy_path(test.pipeline, HAPPY_PATH)
