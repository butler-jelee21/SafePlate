# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import requests
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


base_url = 'https://3da1b925.ngrok.io/query'

data_indices = {
    "business_name": 2,
    "business_address": 3,
    "business_city": 4,
    "business_state": 5,
    "business_postal_code": 6,
    "business_latitude": 7,
    "business_longitude": 8,
    "business_location": 9,
    "business_phone_number": 10,
    "inspection_id": 11,
    "inspection_date": 12,
    "inspection_score": 13,
    "inspection_type": 14,
    "violation_id": 15,
    "violation_description": 16,
    "risk_category": 17
}

permissions = ["write::alexa:household:list", "read::alexa:household:list"]

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        attr = handler_input.attributes_manager.session_attributes
        if not attr:
            attr['business_name'] = 'Unknown'
            attr['business_phone_number'] = 0

        handler_input.attributes_manager.session_attributes = attr
        
        speak_output = (
            "Welcome to Safe Plate, you can search for restaurant health inspection scores by name or phone number or ask for Help. "
            "This skill requires permission to create to do list entries. "
            "Look in the alexa app to grant this permission."
            )
        logger.info("Starting Skill")
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(AskForPermissionsConsentCard(permissions=permissions))
                .ask(speak_output)
                .response
        )


class GetScoreIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetScore")(handler_input)

    def handle(self, handler_input):
        logger.info("In GetScoreIntentHandlerHandler")
        business_name = handler_input.request_envelope.request.intent.slots['Query'].value
        handler_input.attributes_manager.session_attributes['business_name'] = business_name
        logger.info("business_name: {}".format(business_name))

        param = 'name=' + business_name.lower().replace(" ", "+")
        url = base_url + '?' + param
        try:
            res = requests.get(url)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return (
                handler_input.response_builder
                    .speak("Cannot find that restaurant")
                    .response
            )
        
        logger.info("Found restaurant")
        res_json = res.json()
        logger.info(type(res_json))
        inspection_score = res_json['data'][data_indices['inspection_score']][1]
        risk_category = res_json['data'][data_indices['risk_category']][1]
        handler_input.attributes_manager.session_attributes['business_phone_number'] = res_json['data'][data_indices['business_phone_number']][1]
        
        speak_output = (
            "The inspection score of {} is {}. the San Fransisco Health Department classifies this rating as {}. \
            You can get the phone number of this restaurant.".format(business_name, inspection_score, risk_category)
            )
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetNumberIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetNumber")(handler_input)

    def handle(self, handler_input):
        logger.info("In GetNumberIntentHandlerHandler")
        if handler_input.attributes_manager.session_attributes['business_phone_number'] == 0:
            return (
                handler_input.response_builder
                    .speak("Please search for a restaurant first. ")
                    .ask(speak_output)
                    .response
            )

        phone_number = str((handler_input.attributes_manager.session_attributes['business_phone_number'])[0:-2])
        if "n" in phone_number:
            return (
                handler_input.response_builder
                    .speak("Cannot find the phone number. ")
                    .ask("I do not understand. ")
                    .response
            )
        speak_start = "<speak> The phone number is "
        speak_end = "</speak>"
        speak_eff_start = "<say-as interpret-as=" + str('\"') + "digits" + str('\"') + ">"
        speak_eff_body = phone_number
        speak_eff_end = "</say-as>."
        speak_output = (
            str(speak_start + speak_eff_start + speak_eff_body + speak_eff_end + speak_end)
        )
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("I do not understand. ")
                .response
        )

class AddReservationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AddReservation")(handler_input)

    def handle(self, handler_input):
        logger.info("In AddReservationIntentHandlerHandler")
        try:
            
            accessToken = handler_input.req_envelope.context.system.user.permissions.consent_token
        except:
            return (
                handler_input.response_builder
                    .speak("Skill does not have the correct permissions.")
                    .response
            )

        data = {
            "value": ("Make a reservation at {}. The phone number is {}"
                        .format(handler_input.attributes_manager.session_attributes['business_name'], 
                                handler_input.attributes_manager.session_attributes['business_phone_number'])
                    ), 
            "status": "active" 
        }
        header = {
            "Authorization": "Bearer " + accessToken,
            "Content-Type": "json"
        }
        base_req_url = "v2/householdlists/"

        listId = requests.get(base_req_url, header=header)

        header["Content-Type"] = "application/json"

        post_url = "{}{}/items".format(base_req_url, listId)
        res = requests.post(url, header=header, data=data)
        speak_output(
            "Reservation note added to your to do list."
            )
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# class GetNumberIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("GetNumber")(handler_input)

#     def handle(self, handler_input):
#         session_attr = handler_input.attributes_manager.session_attributes
#         query_name = session_attr["Query"]
#         speak_output = ("Finding the phone number of {}".format(query_name))


# class GetRestFromPhoneIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("GetRestFromPhone")(handler_input)

#     def handle(self, handler_input):
#         session_attr = handler_input.attributes_manager.session_attributes
#         query_name = session_attr["Phone_Number"]
#         speak_output = ("Finding the restaurant with the phone number {}".format(query_number))

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

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

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
#sb.add_request_handler(GetNumberIntentHandler())
sb.add_request_handler(GetScoreIntentHandler())
sb.add_request_handler(AddReservationIntentHandler())
#sb.add_request_handler(GetRestFromPhoneIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(GetNumberIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()