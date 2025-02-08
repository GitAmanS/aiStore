from flask import Flask, request, jsonify, render_template, send_from_directory
from functions.run import get_response, context
# enable CORS
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


app.static_folder = 'build'
app.template_folder = 'build'

@app.route('/_next/static/<path:filename>')
def static_files(filename):
    """Serve static files from the _next/static directory.

    This function is used to serve files generated by Next.js at build time.
    """
    
    return send_from_directory(app.static_folder + '/_next/static', filename)

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
