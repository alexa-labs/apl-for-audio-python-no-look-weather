#  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
#  Licensed under the Amazon Software License  http://aws.amazon.com/asl/

# -*- coding: utf-8 -*-
# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import json

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective as APLRenderDoc
from ask_sdk_model.interfaces.alexa.presentation.apla import RenderDocumentDirective as APLARenderDoc

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_supported_interfaces

from ask_sdk_model import Response


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LINKED_DOC = "Link"

class GetWeatherHandler(AbstractRequestHandler):
    """Handler for GetWeather Intent and LaunchRequest"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input) or ask_utils.is_intent_name("GetWeatherIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]
        # the following constants are hardcoded for demo purposes only.
        # In a real skill these values would be pulled from an API
        # set to 2 in order to get the other experience.
        weather_code = 1
        
        # logic to determine which assets should be paired with the forecast
        if weather_code is 1:
            audio = "soundbank://soundlibrary/animals/amzn_sfx_bird_forest_short_01"
            bg_image = "https://images.pexels.com/photos/777211/winter-sunset-purple-sky-777211.jpeg"
            weather_description = "sunny"
            current_temp = 75
        elif weather_code == 2:
            weather_description = "cloudy"
            current_temp = 65
            audio = "soundbank://soundlibrary/nature/amzn_sfx_rain_03"
            bg_image = "https://images.pexels.com/photos/1089455/pexels-photo-1089455.jpeg"
        
        if(get_supported_interfaces(handler_input).alexa_presentation_apl != None):
            visual_data = {"myData": {"bgImage": bg_image, "currentTemp": current_temp, "weatherDescription": weather_description}}
            linked_visual_doc = {"type": LINKED_DOC, "src":"doc://alexa/apl/documents/weather_v"}
            handler_input.response_builder.add_directive(APLRenderDoc(token="apl_doc", document=linked_visual_doc, datasources=visual_data))
        
        # the values above will be inserted into the SSML before it's sent to the APL response
        speak_output = data["translation"]["WEATHER_REPORT"].format(temperature=current_temp, weatherDescription=weather_description)
        
        audio_data = {"myData" : {"ssml": speak_output, "audio": audio}}
        
        linked_audio_doc = {"type": LINKED_DOC, "src":"doc://alexa/apla/documents/weather_a"}
        
        return (
            handler_input.response_builder
                .add_directive(APLARenderDoc(token="aplaDoc", document=linked_audio_doc, datasources=audio_data))
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = data["translation"]["HELP_MESSAGE"]
        speak_reprompt = data["translation"]["HELP_REPROMPT"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_reprompt)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speak_output = data["translation"]["FALLBACK_MESSAGE"]
        speak_reprompt = data["translation"]["FALLBACK_REPROMPT"]
        handler_input.response_builder.speak(speak_output).ask(speak_reprompt)
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = handler_input.attributes_manager.request_attributes["_"]["translation"]["STOP_MESSAGE"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = handler_input.attributes_manager.request_attributes["_"]["translation"]["ERROR_HANDLER"]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale[:2]))

        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        # set default translation data to broader translation
        data = language_data[locale[:2]]
        # if a more specialized translation exists, then select it instead
        # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
        #          then pick that instead
        if locale in language_data:
            data.update(language_data[locale])
        handler_input.attributes_manager.request_attributes["_"] = data

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(GetWeatherHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())
# Register request and response interceptors
sb.add_global_request_interceptor(LocalizationInterceptor())

lambda_handler = sb.lambda_handler()