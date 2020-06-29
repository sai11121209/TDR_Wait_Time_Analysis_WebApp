import tasks


def timed_job():
    tasks.insertdata()
    print("This job is run every three minutes.")


if __name__ == "__main__":
    timed_job()
