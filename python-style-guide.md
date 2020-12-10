# Alexa Cookbook and Sample Skills Style Guide for Python

This Style Guide provides the guidance for how Python code used in this repo should be formatted and laid out. Please use these guidelines (unless you know better ones -- if you do, open an issue/PR). When in doubt, please refer to the official [Python PEP 8 guide](https://www.python.org/dev/peps/pep-0008/).

## Contents

1. Code Layout
1. General
1. Constants, Variables, & Attributes
1. Handlers & Interceptors
1. Boilerplate Code
1. Functions
1. Testing
1. Internationalization (I18N)

## Code Layout
Ensure that the code in lambda_function.py follows this order:
1. License header (if applicable)
1. Constants (not including language strings if multiple languages in the same file)
1. Handlers
1. Functions (if not in separate file)
1. Lambda setup, e.g., `lambda_handler = ...`
1. Language strings (if including multiple languages in the same file)

## General
1. Code needs to be internationalized (use language strings, etc.) but does not need to be translated. Minimum support of en-US required.
1. The `.speak` method should take `speech` as its parameter.
1. The `.reprompt` method should take `reprompt`, `prompt` or `speech` as its parameter.
1. Comments usage:
    1. Indicate what is required/optional action is required.
    1. Mark required actions in comments with `**TODO**`.
    1. Describe key or unusual code.
    1. Describing classes. These should use docstring formatting, and can keep the closing `"""` on the same line for short descriptions, e.g.

        ```python
        class CancelOrStopIntentHandler(AbstractRequestHandler):
            """Handler for Cancel and Stop Intents."""
        ```     
1. To make code more readable, indent and line break statements with multiple conditionals. For example,
    **Do**
    ```python
    return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
    ```
    **Don't**
    This line is too long. Limit all lines to a maximum of 115 characters. Use a line break.
    ```python
    return (is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input))
    ```
    **Don't**
    This line is not indented properly. Four spaces are the preferred indentation method.
    ```python
    return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
    is_intent_name("AMAZON.StopIntent")(handler_input))
    ```
### Constants, Variables & Attributes
1.	Constants, session attributes, and variables should be named in _snake case_ (e.g., `lower_case_with_underscores`).
1.  Class names should use the _CapWords_ convention (e.g., `SkillBuilder`)
1.	Rename boolean variables to begin with "is", "has", "can" or comparable prefix to indicate boolean (e.g. "is_correct", instead of just "correct").

## Handlers & Interceptors
1. If a handler handles exactly one intent/request type, name the handler like <event>Handler (without the AMAZON prefix for built-in intents):
    -	LaunchRequestHandler 
    -	SomeRandomIntentHandler
    -	RepeatIntentHandler
    -	SessionEndedRequestHandler
1. The preferred order for the Handlers when constructing the SkillBuilder:
    1. LaunchRequestHandler
    1. ...skill specific intent handlers...
    1. RepeatIntentHandler (if applicable)
    1. HelpIntentHandler
    1. CancelOrStopIntentHandler
    1. FallbackIntentHandler
    1. SessionEndedRequestHandler
    1. IntentReflectorHandler (for debugging use)
    1. CatchAllExceptionHandler (if applicable)

1. Request and response interceptors should use the suffix **Interceptor** and should include **Request** or **Response** (if specific to that type).
1. The Handlers & Interceptors implementation code should be in the same order as they are added to the SkillBuilder.
1. If a handler is not the only handler for a given intent, include a comment to that effect immediately preceding the `can_handle(...)`, e.g.,
    ```python
    class LaunchRequestHandler(AbstractRequestHandler):
        """This LaunchRequestHandler catches LaunchRequests which are not handled by more specific handlers"""
        def can_handle(self, handler_input)
          ...
    ```

### Boilerplate Code
The code in these sections should be used for their respective handlers. If the functionality of the code requires changes, use this as a baseline.

#### SessionEndedRequestHandler
```python
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for SessionEndedRequest."""
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response
```

#### FallbackHandler
```python
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.FALLBACK_MESSAGE]
        reprompt = data[prompts.FALLBACK_REPROMPT]
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response
```
#### CatchAllExceptionHandler
```python
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, I can't understand the command. Please say again."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
```
#### RequestLogger
```python
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
            handler_input.request_envelope))
```
#### ResponseLogger
```python
class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))
```

## Functions
1. All (non-handler) functions Function names should be lowercase, with words separated by underscores as necessary to improve readability.
2. All functions names should begin with an action verb, e.g., `get_final_score`, `format_casing`, `supports_display`, etc.
3. If a utility function is available in the SDK, the use of it is preferred over using a locally maintain functioned with comparable functionality.

## Testing
1. No specific test methodology is currently required, but do test your code.  Use unit testing (no voice interaction) in addition to voice testing (full stack).
1. Where applicable, include certification testing instructions.

## Internationalization (I18N)
I18N is handled through the [multilingual internationalization module `gettext`](https://docs.python.org/3/library/gettext.html). Follow our localization and internationalization guide at [https://github.com/alexa/skill-sample-python-howto/blob/master/instructions/localization.md](https://github.com/alexa/skill-sample-python-howto/blob/master/instructions/localization.md).

