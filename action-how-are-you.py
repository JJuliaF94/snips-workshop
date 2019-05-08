#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import ConfigParser
from hermes_python.hermes import Hermes
import pyowm
import io


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

INTENT_HOW_ARE_YOU = "JJuliaF94:how_are_you"
INTENT_GOOD = "JJuliaF94:feeling_good"
INTENT_BAD = "JJuliaF94:feeling_bad"
INTENT_ALRIGHT = "JJuliaF94:feeling_alright"

INTENT_FILTER_FEELING = [INTENT_GOOD, INTENT_BAD, INTENT_ALRIGHT]


def main():
    config = read_configuration_file(CONFIG_INI)
    owm = pyowm.OWM(config["secret"]["owm_key"])

    with Hermes("localhost:1883") as h:
        h.owm = owm
        h.subscribe_intent(INTENT_HOW_ARE_YOU, how_are_you_callback) \
         .subscribe_intent(INTENT_GOOD, feeling_good_callback) \
         .subscribe_intent(INTENT_BAD, feeling_bad_callback) \
         .subscribe_intent(INTENT_ALRIGHT, feeling_alright_callback) \
         .start()


def how_are_you_callback(hermes, intent_message):
    session_id = intent_message.session_id

    # set mood according to weather
    config = read_configuration_file(CONFIG_INI)
    observation = hermes.owm.weather_at_place(config["secret"]["city"])
    w = observation.get_weather()
    temp = w.get_temperature('celsius')["temp"]
    if temp >= float(config["secret"]["temperature_threshold"]):
        response = "I'm feeling great! "
    else:
        response = "Not so good. "
    response += "It's {} degrees in {}. How are you?".format(temp, config["secret"]["city"])

    hermes.publish_continue_session(session_id, response, INTENT_FILTER_FEELING)


def feeling_good_callback(hermes, intent_message):
    session_id = intent_message.session_id
    response = "That's awesome! Do you want to hear a joke? What do you call a sheep with no hat and no legs? A cloud. HAA HAA HAA HAA YEAAH"
    hermes.publish_end_session(session_id, response)


def feeling_bad_callback(hermes, intent_message):
    session_id = intent_message.session_id
    response = "Sorry to hear that. Do you want to hear a joke? What do you call a computer that sings? A-Dell. Do you feel better? If not I can give you a knife to make that shit what you call your life an end.HAA HAA HAA HAA YEAAH"
    hermes.publish_end_session(session_id, response)


def feeling_alright_callback(hermes, intent_message):
    session_id = intent_message.session_id
    response = "That's cool. I dont care. Dont talk to me ever again. I dont like you. By by you durk"
    hermes.publish_end_session(session_id, response)


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


if __name__ == "__main__":
    main()
