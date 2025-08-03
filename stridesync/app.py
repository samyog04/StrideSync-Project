from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_logs():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Samyog@944966",
        database="stridesync"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM workout_logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return logs

@app.route("/")
def home():
    logs = get_logs()
    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)

