from app import create_app
import subprocess


app, socketio = create_app()
app.app_context().push()
celery = app.extensions['celery']

def error_handler():

    pass

if __name__=='__main__':

    socketio.run(app, debug=True)





