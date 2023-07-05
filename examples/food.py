import logging
import pathlib

from dff.script import TRANSITIONS, RESPONSE, MISC, PRE_RESPONSE_PROCESSING, GLOBAL, Message, Context
from dff.pipeline import Pipeline
import dff.script.conditions as cnd
import dff.script.labels as lbl

from utils import condition as dm_cnd
from .utils.common import pre_services
from dff.utils.testing import run_interactive_mode
from utils.entity_detection import has_entities, entity_extraction, slot_filling
from utils.generic_responses import generic_response_condition, generic_response_generate


def add_prompt_processing(ctx: Context, pipeline: Pipeline, *args, **kwargs) -> Context:
    if generic_response_condition(ctx, pipeline, *args, **kwargs):
        response = generic_response_generate(ctx, pipeline, *args, **kwargs)
        processed_node = ctx.framework_states["actor"].get("processed_node", ctx.framework_states["actor"]["next_node"])
        dot = '.'
        processed_node.response = Message(text=f"{response}{dot} {processed_node.response}")
        ctx.framework_states["actor"]["processed_node"] = processed_node
    return ctx


script = {
    GLOBAL: {
        PRE_RESPONSE_PROCESSING: {3: add_prompt_processing},
    },
    "food_flow": {
        "start_node": {
            TRANSITIONS: {
                "greeting_node": dm_cnd.is_sf("Open"),
            },
            RESPONSE: Message(text=""),
            MISC: {"speech_functions": ["Open.Attend"]},
        },
        "fallback_node": {
            TRANSITIONS: {},
            RESPONSE: Message(text="I would love to tell you more, but I haven't learnt to do yet!"),
            MISC: {"speech_functions": ["React.Rejoinder.Confront.Challenge.Detach"]},
        },
        "greeting_node": {
            TRANSITIONS: {
                "another_q": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Support.Develop.Extend"),
                        dm_cnd.is_sf("React.Respond.Support.Develop.Elaborate"),
                        dm_cnd.is_sf("React.Respond.Support.Register"),
                        dm_cnd.is_sf("React.Respond.Support.Develop.Enhance"),
                    ]
                ),
                "likes_lasagna": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "doesnt_like_lasagna": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                    ]
                ),
                "confused_bot": cnd.any(
                    [
                        dm_cnd.is_sf("React.Rejoinder.Support.Track.Confirm"),
                        dm_cnd.is_sf("React.Rejoinder.Support.Track.Clarify"),
                        dm_cnd.is_sf("React.Rejoinder.Support.Response.Resolve"),
                    ]
                ),
            },
            RESPONSE: Message(text="Hi! I was thinking about food when you texted... I'm dreaming about lasagna! Do you like it?"),
            MISC: {
                "speech_functions": [
                    "Open.Attend",
                    "Open.Give.Fact",
                    "Sustain.Continue.Prolong.Elaborate",
                    "React.Rejoinder.Support.Track.Clarify",
                ]
            },
        },
        "confused_bot": {
            RESPONSE: Message(text="Oh, I really don't know what to say... Do you want to talk about cuisines of the world?"),
            TRANSITIONS: {
                "doesnt_like_cuisine": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "doesnt_want_to_cook": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"), dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"), dm_cnd.is_midas("neg_answer")]),
                    ]
                ),
            },
            MISC: {
                "speech_functions": ["React.Rejoinder.Support.Develop.Extend", "React.Rejoinder.Support.Track.Clarify"]
            },
        },
        "another_q": {
            RESPONSE: Message(text="Oh, I understand! And do you like pasta?"),
            TRANSITIONS: {
                "likes_lasagna": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "doesnt_like_lasagna": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                    ]
                ),
            },
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "likes_lasagna": {
            TRANSITIONS: {
                "likes_italian": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "doesnt_like_cuisine": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                    ]
                ),
            },
            RESPONSE: Message(text="Oh, we are so similar! So you are a fan of Italian cuisine too, aren't you?"),
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Probe"]},
        },
        "doesnt_like_lasagna": {
            TRANSITIONS: {
                "likes_italian": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "doesnt_like_cuisine": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                    ]
                ),
            },
            RESPONSE: Message(text="Oh :( So you don't like Italian cuisine?"),
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Probe"]},
        },
        "likes_italian": {
            TRANSITIONS: {
                "fav_italian_dish": cnd.any(
                    [dm_cnd.is_sf("React.Rejoinder.Support"), dm_cnd.is_sf("React.Respond.Support")]
                ),
            },
            RESPONSE: Message(text="What's your favorite Italian dish?"),
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "doesnt_like_cuisine": {
            TRANSITIONS: {
                "cuisine": has_entities(["tags:misc"]),
                "fav_cuisine": cnd.all([dm_cnd.is_sf("React")]),
            },
            RESPONSE: Message(text="Then what's your favorite cuisine?"),
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "cuisine": {
            PRE_RESPONSE_PROCESSING: {
                1: entity_extraction(cuisine=["tags:misc"]),
                2: slot_filling,
            },
            RESPONSE: Message(text="Oh, [cuisine]! I just adore it!"),
            TRANSITIONS: {
                "really_likes_cuisine": cnd.exact_match(Message(text="yeah")),
                "doesnt_want_to_cook": dm_cnd.is_sf("React"),
            },
            MISC: {"speech_functions": ["React.Respond.Support.Register", "Sustain.Continue.Prolong.Elaborate"]},
        },
        "fav_italian_dish": {
            TRANSITIONS: {
                "really_likes_cuisine": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "doesnt_want_to_cook": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf("React.Rejoinder.Support.Response.Resolve"),
                        dm_cnd.is_sf("React.Respond.Support.Develop")
                    ]
                ),
            },
            RESPONSE: Message(text="Yeah, I love it too! Have you ever tried to cook it?"),
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "fav_cuisine": {
            TRANSITIONS: {
                "really_likes_cuisine": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all(
                            [
                                cnd.any(
                                    [
                                        dm_cnd.is_sf("React.Rejoinder"),
                                        dm_cnd.is_sf("React.Respond.Support.Develop.Extend"),
                                        dm_cnd.is_sf("React.Respond.Support.Develop.Enhance"),
                                    ]
                                )
                            ]
                        ),
                    ],
                ),
                "doesnt_like_cuisine": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf("React.Rejoinder.Support.Response.Resolve"),
                        cnd.all(
                            [
                                cnd.any(
                                    [
                                        dm_cnd.is_sf("React.Rejoinder"),
                                        dm_cnd.is_sf("React.Respond.Support.Develop.Extend"),
                                        dm_cnd.is_sf("React.Respond.Support.Develop.Enhance"),
                                    ]
                                )
                            ]
                        ),
                    ],
                ),
            },
            RESPONSE: Message(text="Really? Never met a person who liked it!"),
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "doesnt_want_to_cook": {
            TRANSITIONS: {
                "adores_cooking_people": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "cooking_is_trouble": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf("React.Rejoinder.Support.Response.Resolve")
                    ]
                ),
            },
            RESPONSE: Message(text="Okay! And do you like cooking?"),
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "really_likes_cuisine": {
            TRANSITIONS: {
                "adores_cooking_people": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                    ]
                ),
                "cooking_is_trouble": cnd.any(
                    [
                        dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf("React.Rejoinder.Support.Response.Resolve")
                    ]
                ),
            },
            RESPONSE: Message(text="That's so cool, I'd love to learn how to cook it one day! Do you like cooking?"),
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "adores_cooking_people": {
            TRANSITIONS: {
                "say_goodbye": cnd.any(
                    [
                        dm_cnd.is_sf("React"),
                        dm_cnd.is_sf("Open"),
                    ]
                ),
            },
            RESPONSE: Message(text="Wow, I just adore people who know how to cook!"),
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "cooking_is_trouble": {
            TRANSITIONS: {
                "say_goodbye": cnd.any(
                    [
                        dm_cnd.is_sf("React"),
                        dm_cnd.is_sf("Open"),
                    ]
                ),
            },
            RESPONSE: Message(text="Yep, I understand. Usually cooking is just too much trouble."),
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "say_goodbye": {
            TRANSITIONS: {},
            RESPONSE: Message(text="Oh... Sorry, I have to go now. I want to grab some lasagna. Bye!"),
            MISC: {
                "speech_functions": [
                    "React.Respond.Support.Register",
                    "Sustain.Continue.Prolong.Extend",
                    "React.Rejoinder.Confront.Challenge.Detach",
                ]
            },
        },
    },
    # "generic_responses_flow": {
    #     "start_node": {
    #         RESPONSE: Message(text=""),
    #         TRANSITIONS: {"generic_response": generic_response_condition},
    #     },
    #     "generic_response": {
    #         RESPONSE: generic_response_generate,
    #         # TRANSITIONS: {lbl.repeat(): generic_response_condition,
    #         #     ("food_flow", "say_goodbye"): cnd.true()
    #         #     },
    #         TRANSITIONS: {lbl.previous(): cnd.true()},
    #     },
    # },
}

pipeline = Pipeline.from_script(
    script=script,
    start_label=("food_flow", "start_node"),
    fallback_label=("food_flow", "fallback_node"),
    pre_services=pre_services
)

if __name__ == "__main__":
    run_interactive_mode(pipeline)