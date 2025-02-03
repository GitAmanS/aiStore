from flask import Flask, request, jsonify, render_template
from run import get_response, context

app = Flask(__name__)

@app.route('/request', methods=['POST'])
def process_request():
    # write code to compensate for application/x-www-form-urlencoded
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        data = request.get_json()
    response = get_response(data['query'])
    return response
                    

# A simple / route that loads index.html to test /request
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)