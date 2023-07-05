from dff.script import TRANSITIONS, RESPONSE, Message
from dff.pipeline import Pipeline
import dff.script.conditions as cnd
import dff.script.labels as lbl

from utils import condition as loc_cnd
from .utils.common import pre_services
from dff.utils.testing import run_interactive_mode
from utils.generic_responses import generic_response_condition, generic_response_generate

script = {
    "greeting_flow": {
        "start_node": {  # This is an initial node, it doesn't need an `RESPONSE`
            RESPONSE: Message(text=""),
            TRANSITIONS: {"node1": cnd.all([loc_cnd.is_sf("Open.Give.Opinion"), loc_cnd.is_midas("pos_answer")])},
        },
        "node1": {
            RESPONSE: Message(text="Hi, how are you?"),  # When the agent goes to node1, we return "Hi, how are you?"
            TRANSITIONS: {"node2": cnd.exact_match(Message(text="i'm fine, how are you?")),
                          ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
        },
        "node2": {
            RESPONSE: Message(text="Good. I'm glad that you are having a good time."),
            TRANSITIONS: {"node1": cnd.exact_match(Message(text="Hi"))},
        },
        "fallback_node": {  # We get to this node if an error occurred while the agent was running
            RESPONSE: Message(text="Ooops"),
            TRANSITIONS: {"node1": cnd.exact_match(Message(text="Hi"))},
        }
    },
    "generic_responses_flow": {
        "start_node": {
            RESPONSE: Message(text=""),
            TRANSITIONS: {"generic_response": generic_response_condition},
        },
        "generic_response": {
            RESPONSE: generic_response_generate,
            TRANSITIONS: {lbl.repeat(): generic_response_condition},
        },
    }
}

pipeline = Pipeline.from_script(
    script=script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
    pre_services=pre_services
)


if __name__ == "__main__":
    run_interactive_mode(pipeline=pipeline)
# %%
