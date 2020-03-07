from flask import Flask, render_template
import json
from flask_socketio import SocketIO, emit, send
import mysql.connector
import forms


# init the app -------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
database = mysql.connector.connect(
    host="localhost", user="root", passwd="pr09r4mm3r", database="madhu_db1"
)
dbcursor = database.cursor()


# listener for onconnect | socket IO -------------
@socketio.on("connect")
def handle_connected():
    # update chart once connection is established
    update_chart()


# ROUTES ----------
@app.route("/chart")
def template_view():
    # chart view
    return render_template("socket.html")


@app.route("/defects/new", methods=["GET", "POST"])
def defect_new_view():
    # to add a new defect
    form = forms.DefectForm()
    if form.validate_on_submit():
        # form is valid | save to db
        name = form.data["name"]
        dbcursor.execute(
            f'INSERT INTO `defects` (`id`, `name`) VALUES (NULL, "{name}");'
        )
        database.commit()
        # update chart
        update_chart()
        return "success"
    return render_template("defect_form.html", form=form)


@app.route("/vehicles/new", methods=["GET", "POST"])
def vehicle_new_view():
    # to add a new vehicle
    form = forms.VehicleForm()
    if form.validate_on_submit():
        # form is valid | save to db
        value = form.data["value"]
        defect = form.data["defect"]
        dbcursor.execute(
            f"INSERT INTO `vehicles` (`id`, `value`, `defect_id`) VALUES (NULL, '{value}', '{defect}');"
        )
        database.commit()
        # update chart
        update_chart()
        return "success"

    # get defects data | to be used in select field | as foreign key
    dbcursor.execute("SELECT * FROM `defects`")
    defects_data = dbcursor.fetchall()
    return render_template("vehicle_form.html", form=form, defects_data=defects_data)


# HELPERS -----------------
def update_chart():
    """
    This updates the chart using the other helper functions.
    Call this function, when the chart has to updated
    """
    send_data(data=get_data_as_json(), event_name="data_from_server")


def get_data_as_json():
    """
    This function gets data from the database.
    """
    data = [
        {"label": "Venezuela", "value": "290"},
        {"label": "Saudi", "value": "260"},
        {"label": "Canada", "value": "180"},
    ]
    return json.dumps(data)


def send_data(data, event_name):
    """
    This function sends the given data through the socket.
    """
    socketio.emit(event_name, data)


# TO RUN THE APP ------------
if __name__ == "__main__":
    app.run(debug=True)
