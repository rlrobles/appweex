from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

#sensor()
# sched = BackgroundScheduler(daemon=True)
# sched.add_job(sensor,'interval',minutes=1)
# sched.start()

app = Flask(__name__)

@app.route("/home", methods=['GET'])
def home():
    """ Function for test purposes. """
    print("Scheduler is alive!")
    return "Welcome Home :) !"

if __name__ == "__main__":
    app.run(debug=True)