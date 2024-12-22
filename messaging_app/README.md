Build a messaging App with django rest framework
AUTH
    http://127.0.0.1:8000/api-auth/login
    Endpoint: POST /api/signup/

Conversations:

    GET /conversations/ – List all conversations
    POST /conversations/ – Create a new conversation
    GET /conversations/<id>/ – Retrieve a specific conversation
    PUT /conversations/<id>/ – Update a conversation
    DELETE /conversations/<id>/ – Delete a conversation

Messages:

    GET /messages/ – List all messages
    POST /messages/ – Send a new message
    GET /messages/<id>/ – Retrieve a specific message
    PUT /messages/<id>/ – Update a message
    DELETE /messages/<id>/ – Delete a message

** pip freeze > requirements.txt **

pip install djangorestframework
pip install djangorestframework-simplejwt
