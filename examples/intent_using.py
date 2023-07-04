from dff.script import TRANSITIONS, RESPONSE, Message
from dff.pipeline import Pipeline
import dff.script.conditions as cnd

from utils import condition as loc_cnd
from .utils.common import pre_services
from dff.utils.testing import run_interactive_mode


script = {
    "greeting_flow": {
        "start_node": {
            RESPONSE: Message(text=""),
            TRANSITIONS: {"node1": loc_cnd.is_intent("topic_switching")},
        },
        "node1": {
            RESPONSE: Message(text="What do you want to talk about?"),
            TRANSITIONS: {"node2": loc_cnd.is_intent("lets_chat_about")},
        },
        "node2": {
            RESPONSE: Message(text="Ok, what do you want to know?"),
            TRANSITIONS: {"node1": cnd.true()},
        },
    },
}

pipeline = Pipeline.from_script(
    script=script,
    start_label=("greeting_flow", "start_node"),
    pre_services=pre_services
)


if __name__ == "__main__":
    run_interactive_mode(pipeline)
