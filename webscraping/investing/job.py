""" from time import time, sleep
while True:
    sleep(60 - time() % 60)
    print('1')
	# thing to run
 """
import schedule
import time

def job():
    print("I'm working...")
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
""" schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job) """

job()