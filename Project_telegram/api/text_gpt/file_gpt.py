import apiai
import json


async def text_message(message):
    request = apiai.ApiAI(client_access_token="").text_request()
    request.lang = "ru"
    request.session_id = "BatlabAIBot"
    request.query = message.message.text

    response_json = json.loads(request.getresponse().read().decode("utf-8"))
    response = response_json["result"]["fulfillment"]["speech"]
    return response
