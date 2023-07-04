import logging
from dff.script import TRANSITIONS, RESPONSE, MISC
from dff.pipeline import Pipeline
import dff.script.conditions as cnd

from .utils import condition as loc_cnd
from .utils.common import pre_services
from dff.utils.testing import run_interactive_mode

logger = logging.getLogger(__name__)

# Below, `script` is the dialog script.
# A dialog script is a flow dictionary that can contain multiple flows .
# script are needed in order to divide a dialog into sub-dialogs and process them separately.
# For example, the separation can be tied to the topic of the dialog.
# In our example, there is one flow called greeting_flow.

# Inside each flow, we can describe a sub-dialog.
# Here we can also use keyword `LOCAL`, which we have considered in other examples.

# Flow describes a sub-dialog using linked nodes, each node has the keywords `RESPONSE` and `TRANSITIONS`.

# `RESPONSE` - contains the response that the dialog agent will return when transitioning to this node.
# `TRANSITIONS` - describes transitions from the current node to other nodes.
# `TRANSITIONS` are described in pairs:
#      - the node to which the agent will perform the transition
#      - the condition under which to make the transition
script = {
    "greeting_flow": {
        "start_node": {  # This is an initial node, it doesn't need an `RESPONSE`
            RESPONSE: "",
            # TRANSITIONS: {"node1": cnd.exact_match("Hi")},  # If "Hi" == request of user then we make the transition
            TRANSITIONS: {
                "node1": cnd.all([loc_cnd.is_sf("Open.Give.Opinion"), loc_cnd.is_midas("pos_answer")])
            },
            MISC: {"speech_functions": ["start_node"]},
        },
        "node1": {
            RESPONSE: "Hi, how are you?",  # When the agent goes to node1, we return "Hi, how are you?"
            TRANSITIONS: {"node2": cnd.exact_match("i'm fine, how are you?")},
        },
        "new_node": {
            RESPONSE: "Good. What do you want to talk about?",
            TRANSITIONS: {"node3": cnd.exact_match("Let's talk about music.")},
            MISC: {"speech_functions": ["Open.Attend"]},
        },
        "node3": {
            RESPONSE: "Sorry, I can not talk about music now.",
            TRANSITIONS: {"node4": cnd.exact_match("Ok, goodbye.")},
        },
        "node4": {
            RESPONSE: "bye",
            TRANSITIONS: {"node1": cnd.exact_match("Hi")},
            MISC: {"speech_functions": ["Open.Attend"]},
        },
        "fallback_node": {  # We get to this node if an error occurred while the agent was running
            RESPONSE: "Ooops",
            TRANSITIONS: {"node1": cnd.exact_match("Hi")},
            MISC: {"speech_functions": ["fallback_node"]},
        },
    },
}

# A pipeline is an object that processes user input replicas and returns responses
# To create the pipeline, you need to pass the script of the dialogue `script`
# And pass the initial node `start_label`
# and the node to which the pipeline will go in case of an error `fallback_label`
# If `fallback_label` is not set, then its value becomes equal to `start_label` by default
pipeline = Pipeline(
    script=script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
    pre_services=pre_services
)

if __name__ == "__main__":
    run_interactive_mode(pipeline)
