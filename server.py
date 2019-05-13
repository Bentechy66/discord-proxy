from flask import Flask, render_template

from api_routes import api_routes

app = Flask(__name__)

app.register_blueprint(api_routes)

@app.route("/select_guild")
def select_guild():
    return render_template("select_guild.html")

@app.route("/set_token")
def set_token():
    return render_template("set_token.html")

@app.route("/set_theme")
def set_theme():
    return render_template("choose_style.html")

@app.route("/guild/<guild_id>/select_channel")
def select_channel(guild_id):
    return render_template("select_channel.html", guild_id=guild_id)

@app.route("/guild/<guild_id>/<channel_id>")
def guild_channel(guild_id, channel_id):
    return render_template("guild_channel_messages.html", guild_id=guild_id, channel_id=channel_id)

app.run("0.0.0.0", 5000, debug=True)