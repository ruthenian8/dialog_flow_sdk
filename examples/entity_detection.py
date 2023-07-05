from dff.pipeline.pipeline.pipeline import Pipeline
from dff.script import TRANSITIONS, RESPONSE, PRE_TRANSITIONS_PROCESSING, Context, Message
import dff.script.conditions as cnd
from utils import condition as dm_cnd
from dff.script import slots
from dff.script.slots import conditions as slot_cnd
from dff.script.slots import response as slot_rsp
from dff.script.slots import processing as slot_proc

from dff.pipeline import Pipeline

from .utils.common import pre_services
from dff.utils.testing import run_interactive_mode
from utils.entity_detection import get_entity_by_tag, get_entity_by_type


class ContextAwareSlot(slots.FunctionSlot):
    def extract_value(self, ctx: Context, pipeline: Pipeline):
        self.value = str(self.func(ctx, pipeline))
        return self.value


person_slot = ContextAwareSlot(name="tags:person", func=get_entity_by_tag("person"))
videoname_slot = ContextAwareSlot(name="tags:videoname", func=get_entity_by_tag("videoname"))
wiki_slot = ContextAwareSlot(name="wiki:Q177220", func=get_entity_by_type("Q177220"))

script = {
    "greeting_flow": {
        "start_node": {  # This is an initial node, it doesn't need an `RESPONSE`
            RESPONSE: Message(text=""),
            TRANSITIONS: {"node1": cnd.all([dm_cnd.is_midas("pos_answer")])},
        },
        "node1": {
            RESPONSE: Message(text="Hi, how are you?"),  # When the agent goes to node1, we return "Hi, how are you?"
            TRANSITIONS: {"node2": cnd.exact_match(Message(text="i'm fine, how are you?"))},
        },
        "node2": {
            RESPONSE: Message(text="Good. What do you want to talk about?"),
            TRANSITIONS: {
                "node3": cnd.exact_match(Message(text="Let's talk about music."))
            },
        },
        "node3": {
            RESPONSE: Message(text="What is your favourite singer?"),
            PRE_TRANSITIONS_PROCESSING: {
                "extract_slots": slot_proc.extract(["tags:person", "tags:videoname", "wiki:Q177220"])
            },
            TRANSITIONS: {"node4": slot_cnd.is_set_any(["tags:person", "tags:videoname", "wiki:Q177220"])},
        },
        "node4": {
            RESPONSE: slot_rsp.fill_template(
                Message(text="I also like {tags:person} songs.")
            ),
            TRANSITIONS: {"node5": cnd.exact_match(Message(text="Ok, goodbye."))},
        },
        "node5": {
            RESPONSE: Message(text="bye"),
            TRANSITIONS: {"node1": cnd.exact_match(Message(text="Hi"))},
        },
        "fallback_node": {  # We get to this node if an error occurred while the agent was running
            RESPONSE: Message(text="Ooops"),
            TRANSITIONS: {"node1": cnd.exact_match(Message(text="Hi"))},
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
