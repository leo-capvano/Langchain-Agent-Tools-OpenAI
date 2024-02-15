import logging
# Fixing MIME types for static files under Windows
import mimetypes
import os

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))  # Load environment variables from .env file

app = Flask(__name__)


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)


@app.route("/api/conversation/custom", methods=["GET", "POST"])
def conversation_custom():
    from utilities.helpers.OrchestratorHelper import Orchestrator
    message_orchestrator = Orchestrator()

    try:
        user_message = request.json["messages"][-1]['content']
        conversation_id = request.json["conversation_id"]
        user_assistant_messages = list(
            filter(lambda x: x['role'] in ('user', 'assistant'), request.json["messages"][0:-1]))
        chat_history = []
        for index, user_msg in enumerate(user_assistant_messages):
            if index % 2 == 0:
                assistant_msg = user_assistant_messages[index + 1]['content']
                if assistant_msg != "Ok, I will remember what you told me!":
                    chat_history.append((user_assistant_messages[index]['content'], assistant_msg))
        from utilities.helpers.ConfigHelper import ConfigHelper
        messages = message_orchestrator.handle_message(user_message=user_message, chat_history=chat_history,
                                                       conversation_id=conversation_id,
                                                       orchestrator=ConfigHelper.get_active_config_or_default().orchestrator)

        response_obj = {
            "id": "response.id",
            "model": os.getenv("AZURE_OPENAI_MODEL"),
            "created": "response.created",
            "object": "response.object",
            "choices": [{
                "messages": messages
            }]
        }

        return jsonify(response_obj), 200

    except Exception as e:
        errorMessage = str(e)
        logging.exception(f"Exception in /api/conversation/custom | {errorMessage}")
        return jsonify({"error": "Exception in /api/conversation/custom. See log for more details."}), 500


if __name__ == "__main__":
    app.run()
