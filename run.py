from gigavisor import app, socketio


# Run apps from Python interpreter, in debug mode
if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, host='0.0.0.0', port=5000)
