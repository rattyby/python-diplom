from celery import Celery


app = Celery(broker='redis://127.0.0.1:6379/1', backend='redis://127.0.0.1:6379/2', )


@app.task()
def send_email():
    """
    Так как сервера почты нет, то реализация функции отсутствует
    """
    pass
