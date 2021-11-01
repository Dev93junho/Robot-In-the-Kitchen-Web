"""
This app is contoller for Kitchen Master2
Written by Junho Shin, 09-2021
"""
#!/usr/bin/env python
#coding: utf-8


from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

app = Flask(__name__) # Flask object instance 
app.secret_key = "secret"
socketio = SocketIO(app)

user_no = 1

@app.route('/') #url routing
def index(): # View function call 
    return render_template('index.html') # template, seem to user

# Login function
# If User isn't join this controller, go to join function
@app.route('/login')
def login():
    pass

# Join function
# If User will have joined this controller, back to login function
@app.route('/join')
def join():
    pass

@app.route('/control')
def control():
    pass


if __name__ == '__main__':
    app.run(port = 8000, debug=True)



