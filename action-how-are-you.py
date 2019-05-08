#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from hermes_python.hermes import Hermes
from random import choice

INTENT_HOW_ARE_YOU = "JJuliaF94:how_are_you"


def main():
    with Hermes("localhost:1883") as h:
        h.subscribe_intent(INTENT_HOW_ARE_YOU, how_are_you_callback) \
         .start()


def how_are_you_callback(hermes, intent_message):
    answers = ["bad", "I hate my life", "give me a window", "i love you", "life is wonderful", "i am a duck"]
    session_id = intent_message.session_id
    response = choice(answers)
    hermes.publish_end_session(session_id, response)


if __name__ == "__main__":
    main()
