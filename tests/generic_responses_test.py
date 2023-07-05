from dff.utils.testing import check_happy_path
from dff.script import Message
from examples import generic_responses as test

# testing
HAPPY_PATH = [
    (Message(text="Hi"), Message(text="Hi, how are you?")),  # start_node -> node1
    (Message(text="I'm fine, square root of two times square root of three is square root of six is it?"), Message(text="Yes")),  # node1 -> generic_response
    (Message(text="Ok"), Message(text="Ooops")),  # generic_response -> fallback_node
]


if __name__ == "__main__":
    check_happy_path(test.pipeline, HAPPY_PATH)
