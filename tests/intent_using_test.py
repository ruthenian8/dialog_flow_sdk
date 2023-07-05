from dff.utils.testing import check_happy_path
from dff.script import Message
from examples import intent_using as test

# testing
HAPPY_PATH = [
    (Message(text="tell me something else"), Message(text="What do you want to talk about?")),  # start_node -> node1
    (Message(text="let's chat about you"), Message(text="Ok, what do you want to know?")),  # node1 -> node2
]


if __name__ == "__main__":
    check_happy_path(test.pipeline, HAPPY_PATH)
