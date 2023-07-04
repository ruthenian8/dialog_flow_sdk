from dff.utils.testing import check_happy_path
from examples import intent_using as test

# testing
HAPPY_PATH = [
    ("tell me something else", "What do you want to talk about?"),  # start_node -> node1
    ("let's chat about you", "Ok, what do you want to know?"),  # node1 -> node2
]


if __name__ == "__main__":
    check_happy_path(test.pipeline, HAPPY_PATH)
