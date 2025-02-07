from flask import Flask, request, jsonify, render_template
from run import get_response, context
# enable CORS
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

@app.route('/request', methods=['POST'])
def process_request():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        data = request.get_json()
    response = get_response(data['query'])
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/context-clear')
def clear_context():
    global context
    context = []
    return 'Context cleared'


@app.route('/context/update', methods=['POST'])
def update_context():
    global context
    data = request.get_json()
    context = data['context']
    return jsonify(context)

if __name__ == '__main__':
    app.run(debug=True)