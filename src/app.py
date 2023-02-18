# To create our first server, we need to add the following two lines to any python file:

from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

# After creating our app, we need to run and start the application.

# When the application runs, it will take over the command line. Typing on it will not be possible because a server application
# (like Flask) never stops running, it keeps waiting for "requests" forever.

## REMEMBER: Each endpoint in a Flask API is represented by a function and a decorator like this:

# @app.route('/blabla', methods=['GET'])        #   This line specifies the enpoint that will be available from now on (in this case
                                                #   DOMAIN/blabla) as well as the methods that will be used with that URL —in this case
                                                #   the 'GET' method (for reading data).
                                                #
                                                #   @app.route is a decorator that turns a regular Python function into a Flask view
                                                #   function, which converts the function’s return value into an HTTP response to be
                                                #   displayed by an HTTP client, such as a web browser.
                                                #
                                                #   @app.route("/xxx") is a Python decorator that Flask provides to assign URLs in
                                                #   our app to functions. […] Python decorators are essentially logic which "wraps"
                                                #   other functions; they always match the syntax of being a line above the function
                                                #   they're modifying.
                                                #
                                                #   In addition to accepting the URL of a route as a parameter, the @app.route() decorator
                                                #   can accept a second argument: a list of accepted HTTP methods. `GET` is the default.
                                                #
# def hello_world():                            #   This line defines a function that will be called by Flask when that endpoint
                                                #   is called by the user (when the user requests DOMAIN/blabla).
#    return 'Hello, World!'                     #   The third line returns the text: "Hello World" to the requesting client or browser.

# REST APIs have to return data in JSON format. You can use Flask' `jsonify` function to easily convert any of the basic data-types
# to JSON data like this:

    # add the jsonify method to your Flask import
        # from flask import Flask, jsonify

    # Variable with the data we want to display thru our API
        # data = { "name": "Bobby", "lastname": "Rixer" }

    # @app.route('/blahblah', methods=['GET'])
        # def hello_world():
            # data_converted_to_json = jsonify(data)           ==> Converts the variable 'data' into a JSON string
            # return json_text                                 ==> returns  [ { "lastname": "Rixer", "name": "Bobby" } ]   

# Defining the variable I will be stroing my data at:

tasks = [                                                      #   Variable declared **outside** the function (global scope)
    { "label": "Washing dishes", "done": False },
    { "label": "Doing laundry", "done": False }
]

# Defining the first endpoint — URL: '/tasks', METHOD: 'GET'

@app.route('/tasks', methods=['GET'])
def which_are_my_tasks():
    tasks_converted_to_json = jsonify(tasks)
    return tasks_converted_to_json

# At this point, http://192.168.100.12:3245/tasks returns [{"done":false,"label":"Washing dishes"},{"done":false,"label":"Doing laundry"}]

# Defining the second endpoint — URL: '/tasks', METHOD: 'POST'

# This time, we are expecting to receive the tasks that the client wants to add inside of the request body.

# The request body is already JSON-decoded, and it comes in the request.json variable ?????????????????????

@app.route('/tasks', methods=['POST'])                          #   This line specifies the enpoint that will be available from now on
                                                                #   (in this case at DOMAIN/tasks) as well as the methods that will be
                                                                #   used with that URL —in this case the 'POST' method (for updating data).
def add_new_task():                                             #   This line defines a function that will be called by Flask when the
                                                                #   endpoint `/todos/<int:position>` is called by the user
                                                                #   (at DOMAIN/tasks) using the method 'POST').
    request_body = request.json                                 #   Declara la variable request_body y asígnale el valor... ¿¡!?
                                                                #   What is `request`?
                                                                #   What is `json`?
    tasks.append(request_body)                                  #   Take the `tasks` list (?) and add (append) what we have stored in the
                                                                #   variable `request_body`` as last element.
    return jsonify(tasks)                                       #   Return the JSON-ification of the resulting list (?).

#   Making sure that the request body is being duly converted into a real Python data structure —like a dictionary.

#   We already used request.json for that, since we know that the request will be in format application/json ?????????????????????

#   If that is not known, you may want to use `request.get_json(force=True)` to ignore the content type and treat it like json.


@app.route('/tasks/<int:position>', methods=['DELETE'])         #   The main difference here is that, as we can see, the request with the
                                                                #   DELETE method is made thru the endpoint (URL) `/todos/<position:int>`.
                                                                #   This is, the URL must receive the position of the task to delete as part
                                                                #   of itself.
def delete_todo(position):                                      #   This line defines a function that will be called by Flask when the
                                                                #   endpoint `/tasks/<int:position>` is called by the user
                                                                #   (at DOMAIN/tasks/<int:position>) using the method 'DELETE'). In addition,
                                                                #   this function will require a parameter this time (`position`).
    tasks.pop(position - 1)                                     #   The function will execute the method `.pop()` on the list `tasks`, passing
                                                                #   `position - 1` as parameter. The `- 1` has to do with the fact that lists
                                                                #   are 0-index. Thus, position [1] should be actually calling for the deletion
                                                                #   of tasks[0], so on and so forth.
    return jsonify(tasks)                                       #   Return the JSON-ification of the resulting list (?).

#   These two lines should always be at the end of your app.py file.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)

#   When the new server is run by opening a new separate terminal and entering the command `pipenv run python src/app.py`, Terminal should return
#   something like:

#   Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
#       * Serving Flask app 'app' (lazy loading)
#       * Environment: production
#       WARNING: This is a development server. Do not use it in a production deployment.
#       Use a production WSGI server instead.
#       * Debug mode: on
#       * Running on all addresses (0.0.0.0)
#       WARNING: This is a development server. Do not use it in a production deployment.
#       * Running on http://127.0.0.1:3245
#       * Running on http://192.168.100.12:3245 (Press CTRL+C to quit)
#       * Restarting with stat
#       * Debugger is active!
#       * Debugger PIN: 119-144-370

#   From then on all requests made thru the API should have an effect on the Terminal, such as, for instance:
#   127.0.0.1 - - [18/Feb/2023 09:31:37] "GET / HTTP/1.1" 404 -
#   127.0.0.1 - - [18/Feb/2023 09:31:53] "GET /tasks HTTP/1.1" 200 -
