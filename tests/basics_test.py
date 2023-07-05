from dff.utils.testing import check_happy_path
from dff.script import Message
from examples import basics as test

# testing
HAPPY_PATH = [
    (Message(text="Hi"), Message(text="Hi, how are you?")),  # start_node -> node1
    (Message(text="i'm fine, how are you?"), Message(text="Good. What do you want to talk about?")),  # node1 -> node2
    (Message(text="Let's talk about music."), Message(text="Sorry, I can not talk about music now.")),  # node2 -> node3
    (Message(text="Ok, goodbye."), Message(text="bye")),  # node3 -> node4
    (Message(text="Hi"), Message(text="Hi, how are you?")),  # node4 -> node1
    (Message(text="stop"), Message(text="Ooops")),  # node1 -> fallback_node
    (Message(text="stop"), Message(text="Ooops")),  # fallback_node -> fallback_node
    (Message(text="Hi"), Message(text="Hi, how are you?")),  # fallback_node -> node1
    (Message(text="i'm fine, how are you?"), Message(text="Good. What do you want to talk about?")),  # node1 -> node2
    (Message(text="Let's talk about music."), Message(text="Sorry, I can not talk about music now.")),  # node2 -> node3
    (Message(text="Ok, goodbye."), Message(text="bye")),  # node3 -> node4
]


if __name__ == "__main__":
    check_happy_path(test.pipeline, HAPPY_PATH)
