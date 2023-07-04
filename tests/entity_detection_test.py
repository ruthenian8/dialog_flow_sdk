from dff.script import Message
from dff.utils.testing import check_happy_path
from examples import entity_detection as test

# testing
HAPPY_PATH = [
    (Message(text="Hi"), Message(text="Hi, how are you?")),  # start_node -> node1
    (Message(text="i'm fine, how are you?"), Message(text="Good. What do you want to talk about?")),  # node1 -> node2
    (Message(text="Let's talk about music."), Message(text="What is your favourite singer?")),  # node2 -> node3
    (Message(text="Kurt Cobain."), Message(text="I also like kurt cobain songs.")),  # node3 -> node4
    (Message(text="Ok, goodbye."), Message(text="bye")),  # node4 -> node5
]


if __name__ == "__main__":
    check_happy_path(test.pipeline, HAPPY_PATH)
