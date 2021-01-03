from Config import app
import flask
from flask import jsonify,request,abort

import T2Service
from AIService import chatbot_response



books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/ai/v1/command', methods=['POST'])
def command():
    if not request.json or not 'command' in request.json:
        abort(400)

    res= chatbot_response(request.json['command'])
    print(res)
    return jsonify(res)

@app.route('/voice/v1/say', methods=['POST'])
def say():
    if not request.json or not 'command' in request.json:
        abort(400)
    T2Service.say(request.json['command'])
    return jsonify(request.json)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    #task = [task for task in tasks if task['id'] == task_id]
    #if len(task) == 0:
     #   abort(404)
    #return jsonify({'task': task[0]})
    return None

if __name__ == '__main__':
    app.run(debug=True,threaded=False)

#if __name__ == '__main__':
#app.run(host='0.0.0.0', port=80)