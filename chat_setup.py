from celery import Celery

app = Celery('ChattyTasks', broker='amqp://guest@localhost//')

@app.task
def message_received(message):
    print "Somebody received a message: {0}".format(message)

