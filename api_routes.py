import requests

from flask import Blueprint, jsonify, request
from json import loads

api_routes = Blueprint("api_routes", __name__, url_prefix="/api")

def get_api_response(endpoint, token):
    '''Gets a response from Discord's api from the provided endpoint with the supplied token.'''
    if endpoint[0] == "/":
        endpoint = endpoint[1:] # Remove prepended / from api route
    res = requests.get(f"https://discordapp.com/api/{endpoint}", headers={"authorization": token})
    return loads(res.content)

#
# General routes
#

@api_routes.route('/user_data', methods=["POST"])
def user_data():
    '''Returns a user's information.
    Requires a token to be passed via POST in the form token=x'''
    data = request.form
    user_data = get_api_response("/users/@me", data.token)
    return jsonify(user_data)

@api_routes.route('/guilds', methods=["POST"])
def guilds():
    '''Returns a user's guilds.
    Requires a token to be passed via POST in the form token=x'''
    data = request.form
    guilds = get_api_response("/users/@me/guilds", data["token"])
    return jsonify(guilds)

#
# Guild-based routes
#
@api_routes.route('/guild/<id>/channels', methods=["POST"])
def guild_channels(id):
    '''Return a guild's channels (An array of challenge objects).
    Requires a token to be passed via POST in the form token=x, and a guild ID as the id parameter'''
    data = request.form
    guild_channels = get_api_response(f"/guilds/{id}/channels", data["token"])
    return jsonify(guild_channels)

#
# Channel-based routes
#
@api_routes.route('/channel/<id>/messages', methods=["POST"])
def channel_messages(id):
    '''Return a channel's messages
    Returns the 50 most recent messages from a given channel
    Requires a token to be passed via POST in the form token=x, and a channel ID as the id parameter.'''
    data = request.form
    channel_messages = get_api_response(f"/channels/{id}/messages", data["token"])
    return jsonify(channel_messages)

@api_routes.route('/channel/<id>/send_message', methods=["POST"])
def send_message(id):
    '''Sends a message from the user's account
    Requires a token to be passed via POST in the form token=x, message data via POST in the form message=y, and a channel ID as the id parameter.'''
    data = request.form
    res = requests.post(f"https://discordapp.com/api/channels/{id}/messages", json={"content": data["message"]}, headers={"authorization": data["token"], "content-type": "application/json"})
    return jsonify(res.content)