# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:20:05 2019

@author: nigentili
"""


# variables  : -intentMessage
#              -hermes     

required_slots = {  # We are expecting these slots.
    "formato": None,
    "tipo": None
    }

conf['global']['formatoCoffe']
conf['global']['tipoCoffe']

# make coffè call back 
current_session_id = intentMessage.session_id

formatoCoffe_slot = intentMessage.slots.coffeeFormat.first().value or conf['global']['formatoCoffe']
tipoCoffe_slot    = intentMessage.slots.coffeeType.first().value or conf['global']['tipoCoffe']

conf['global']['formatoCoffe'] = formatoCoffe_slot
conf['global']['tipoCoffe'] = tipoCoffe_slot

if not formatoCoffe_slot:
    result_sentence = "Certo! Come lo preferisci? Corto,lungo o espresso ?"
    return hermes.publish_continue_session(current_session_id,
                                               result_sentence,
                                               ["makeCoffee"])
                                               
if not tipoCoffe_slot:
    result_sentence = "Come lo preferisci? Schiumato,macchiato o decaffeinato ?"
    return hermes.publish_continue_session(current_session_id,
                                               result_sentence,
                                               ["makeCoffee"])

result_sentence = "Caffè {} {} in preparazione.".format(tipoCoffe_slot,formatoCoffe_slot)
conf['global']['formatoCoffe'] = None
conf['global']['tipoCoffe'] = None
return hermes.publish_end_session(current_session_id, result_sentence)




# make Tè call back 
current_session_id = intentMessage.session_id

formatoTe_slot = intentMessage.slots.teaFormat.first().value


if not formatoTe_slot:
    result_sentence = "Come lo preferisci? Grande, medio o piccolo ?"
    return hermes.publish_continue_session(current_session_id,
                                               result_sentence,
                                               ["makeTea"])

result_sentence = "Tè {} in preparazione.".format(formatoTe_slot)
return hermes.publish_end_session(current_session_id, result_sentence)





# make chock call back 
current_session_id = intentMessage.session_id

formatoChock_slot = intentMessage.slots.chockFormat.first().value


if not formatoChock_slot:
    result_sentence = "Come la preferisci? Grande, media o piccola ?"
    return hermes.publish_continue_session(current_session_id,
                                               result_sentence,
                                               ["makeChock"])

result_sentence = "Cioccolata {} in preparazione.".format(formatoChock_slot)
return hermes.publish_end_session(current_session_id, result_sentence)






if len(intentMessage.slots.coffeType) > 0:
    coffeType = intentMessage.slots.coffeType.first().value # We extract the value from the slot "house_room"
    result_sentence = "ok. I'm making a {} coffee.".format(str(coffeType))  # The response that will be said out loud by the TTS engine.
else:
    result_sentence = ""

current_session_id = intentMessage.session_id
hermes.publish_end_session(current_session_id, result_sentence)





















