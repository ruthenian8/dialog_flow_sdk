import logging

from dff.script import TRANSITIONS, RESPONSE, MISC, Message
from dff.pipeline import Pipeline

from .utils.common import pre_services
from dff.utils.testing import run_interactive_mode


logger = logging.getLogger(__name__)

script = {
    "food_flow": {
        "start_node": {
            TRANSITIONS: {},
            RESPONSE: Message(text=""),
            MISC: {"speech_functions": ["Open.Attend"]},
        },
        "fallback_node": {
            TRANSITIONS: {},
            RESPONSE: Message(text="Ooops"),
            MISC: {"speech_functions": ["fallback_node"]}
        },
    },
}

pipeline = Pipeline.from_script(
    script=script,
    start_label=("food_flow", "start_node"),
    fallback_label=("food_flow", "fallback_node"),
    pre_services=pre_services
)


if __name__ == "__main__":
    run_interactive_mode(pipeline)
