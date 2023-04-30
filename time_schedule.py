import threading
import schedule
import time
'''
def job():
    print("工作1  ",time.strftime("%H:%M:%S"))
def job2():
    print('工作2  ',time.strftime("%H:%M:%S"))
def job3():
    print('工作3  ',time.strftime("%H:%M:%S"))
# 每(n)秒/分/時/天/週執行(job)
#schedule.every(10).seconds.do(job)
#schedule.every(1).seconds.do(job2)
#schedule.every(1).minutes.do(job)
#schedule.every(3).hours.do(job)
#schedule.every(3).days.do(job)
#schedule.every(3).weeks.do(job)
## at:每分鐘的第(n)秒時執行
#schedule.every().minute.at(":23").do(job3)
def run():
    schedule.every(1).seconds.do(job2)
    while True:
        schedule.run_pending()
        time.sleep(1)
'''


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def background_job():
    print('Hello ',time.strftime("%H:%M:%S"))


schedule.every(3).seconds.do(background_job)

# Start the background thread
stop_run_continuously = run_continuously()

# Do some other things...
#time.sleep(10)

# Stop the background thread
#stop_run_continuously.set()