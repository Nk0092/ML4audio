#!/usr/bin/env python3.7

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes

# imported to get type check and IDE completion
from hermes_python.ontology.dialogue.intent import IntentMessage

CONFIG_INI = "config.ini"

# if this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
#
# hint: MQTT server is always running on the master device
MQTT_IP_ADDR: str = "localhost"
MQTT_PORT: int = 1883
MQTT_ADDR: str = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


MAKE_COFFE = 'makeCoffee'
MAKE_TEA = 'makeTea'
MAKE_CHOC = 'makeChoc'


coffee_dict_slot = {
    "formatoCoffe": None,
    "tipoCoffe": None
}

SessionsStates = {}

# class coffeeApp:
#     """class used to wrap action code with mqtt connection
#        please change the name referring to your application
#     """

#     def __init__(self):
#         # get the configuration if needed
#         try:
#             self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
#         except Exception:
#             self.config = None

#         # start listening to MQTT
#         self.start_blocking()


#@staticmethod
def makeCoffee(hermes: Hermes, intent_message: IntentMessage):
    
    current_session_id = intent_message.session_id
    formatoCoffe_slot = intent_message.slots.coffeeFormat.first().value or coffee_dict_slot['formatoCoffe']
    tipoCoffe_slot = intent_message.slots.coffeeType.first().value or coffee_dict_slot['tipoCoffe']

    coffee_dict_slot['formatoCoffe'] = formatoCoffe_slot
    coffee_dict_slot['tipoCoffe'] = tipoCoffe_slot

    if not formatoCoffe_slot:
        result_sentence = "Certo! Come lo preferisci? Corto,lungo o espresso?"
        return hermes.publish_continue_session(current_session_id, result_sentence, [MAKE_COFFE])
                                                
    if not tipoCoffe_slot:
        result_sentence = "Come lo preferisci? Schiumato,macchiato o decaffeinato?"
        return hermes.publish_continue_session(current_session_id, result_sentence, [MAKE_COFFE])

    result_sentence = "Caffè {} {} in preparazione.".format(tipoCoffe_slot,formatoCoffe_slot)
    coffee_dict_slot['formatoCoffe'] = None
    coffee_dict_slot['tipoCoffe'] = None
    hermes.publish_end_session(current_session_id, result_sentence)


#@staticmethod
def makeChoc(hermes: Hermes, intent_message: IntentMessage):
    
    current_session_id = intent_message.session_id
    formatoChoc_slot = intent_message.slots.chocFormat.first().value

    if not formatoChoc_slot:
        result_sentence = "Certo! Come la preferisci? Grande, media o piccola?"
        return hermes.publish_continue_session(current_session_id, result_sentence, [MAKE_CHOC])
                                        
    result_sentence = "Cioccolata {} in preparazione.".format(formatoChoc_slot)
    hermes.publish_end_session(current_session_id, result_sentence)


#@staticmethod
def makeTea(hermes: Hermes, intent_message: IntentMessage):

    current_session_id = intent_message.session_id
    formatoTea_slot = intent_message.slots.teaFormat.first().value

    if not formatoTea_slot:
        result_sentence = "Certo! Come lo preferisci? Grande, medio o piccolo?"
        return hermes.publish_continue_session(current_session_id, result_sentence, [MAKE_TEA])
                                        
    result_sentence = "Tè {} in preparazione.".format(formatoTea_slot)
    hermes.publish_end_session(current_session_id, result_sentence)


def session_started(hermes, session_started_message):
    print("Session Started")

    print("sessionID: {}".format(session_started_message.session_id))
    print("session site ID: {}".format(session_started_message.site_id))
    print("sessionID: {}".format(session_started_message.custom_data))

    session_id = session_started_message.session_id
    custom_data = session_started_message.custom_data

    if custom_data:
        if SessionsStates.get(custom_data):
            SessionsStates[session_id] = SessionsStates[custom_data]
            SessionsStates.pop(custom_data)


def session_ended(hermes, session_ended_message):
    print("Session Ended")
    session_id = session_ended_message.session_id
    session_site_id = session_ended_message.site_id

    if SessionsStates.get(session_id) is not None:
        hermes.publish_start_session_action(site_id=session_site_id,
                                            session_init_text="",
                                            session_init_can_be_enqueued=False,
                                            custom_data=session_id)




# register callback function to its intent and start listen to MQTT bus
with Hermes(MQTT_ADDR) as h:
    h.subscribe_intent(MAKE_COFFE, makeCoffee)\
    .subscribe_intent(MAKE_CHOC, makeChoc)\
    .subscribe_intent(MAKE_TEA, makeTea)\
    .subscribe_session_ended(session_ended) \
    .subscribe_session_started(session_started)\
    .start()
        

