import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Base WebSocket consumer. Provides a general encapsulation for the
    WebSocket handling model that other applications can build on.
    """

    def connect(self):
        """
        Accepts an incoming socket
        """
        self.accept()

    def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed.
        """

    def receive(self, text_data):
        """
        Called with a decoded WebSocket frame.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
