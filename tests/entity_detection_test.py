from dff.utils.testing import check_happy_path
from examples import entity_detection as test

# testing
HAPPY_PATH = [
    ("Hi", "Hi, how are you?"),  # start_node -> node1
    ("i'm fine, how are you?", "Good. What do you want to talk about?"),  # node1 -> node2
    ("Let's talk about music.", "What is your favourite singer?"),  # node2 -> node3
    ("Kurt Cobain.", "I also like kurt cobain songs."),  # node3 -> node4
    ("Ok, goodbye.", "bye"),  # node4 -> node5
]


if __name__ == "__main__":
    check_happy_path(test.pipeline, HAPPY_PATH)
