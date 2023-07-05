import logging

from dff.script import TRANSITIONS, RESPONSE, MISC, Message
from dff.pipeline import Pipeline
import dff.script.conditions as cnd

from utils import condition as loc_cnd
from .utils.common import pre_services
from dff.utils.testing import run_interactive_mode


logger = logging.getLogger(__name__)

script = {
    "greeting_flow": {
        "start_node": {
            TRANSITIONS: {"greet_and_ask_about_pets": cnd.all([loc_cnd.is_sf("Open.Demand.Fact")])},
            RESPONSE: Message(text="Hi %username%!"),
            MISC: {"speech_functions": ["Open.Attend"]},
        },
        "fallback_node": {TRANSITIONS: {}, RESPONSE: Message(text="Ooops")},
        "greet_and_ask_about_pets": {
            TRANSITIONS: {
                "cool_and_clarify_which_pets": cnd.any(
                    [
                        cnd.any(
                            [
                                loc_cnd.is_sf("React.Respond.Support.Reply.Agree"),
                                loc_cnd.is_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all([loc_cnd.is_sf("React.Rejoinder"), loc_cnd.is_midas("pos_answer")]),
                    ]
                ),
                "sad_and_say_about_pets": cnd.any(
                    [
                        loc_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        cnd.all([loc_cnd.is_sf("React.Rejoinder"), loc_cnd.is_midas("neg_answer")]),
                    ]
                ),
            },
            RESPONSE: Message(text="I'm fine. Jack, a friend of mine told me about their new cat, Lucy. Do you like pets?"),
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "cool_and_clarify_which_pets": {
            TRANSITIONS: {
                "tell_me_more_about_fav_pets": cnd.all([loc_cnd.is_sf("React.Rejoinder.Support.Response.Resolve")])
            },
            RESPONSE: Message(text="Oh, cool! What animals do you like the most?"),
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "sad_and_say_about_pets": {
            TRANSITIONS: {},
            RESPONSE: Message(text="Oh, that's sad! Why is it so?"),
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "tell_me_more_about_fav_pets": {
            TRANSITIONS: {},
            RESPONSE: Message(text="That's rather lovely! I like them, too!"),
            MISC: {"speech_functions": ["React.Respond.Support.Reply.Affirm"]},
        },
    },
}

pipeline = Pipeline.from_script(
    script=script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
    pre_services=pre_services
)

if __name__ == "__main__":
    run_interactive_mode(pipeline)
