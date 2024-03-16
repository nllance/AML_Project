from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from algorithm_layer import process_image, text_to_dict
from database_layer import store_data, query_data

app = Flask(__name__)
app.secret_key = 'GUeierToUte836383d99H'

# Render the HTML template for user input
@app.route('/')
def index():
    return render_template('index.html')

# Handle image uploads and user information
@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

# Process the image
@app.route('/process_upload', methods=['POST'])
def process_upload():
    image = request.files.get('image')
    result = process_image(image)
    if result['status'] == 'success':
        data = text_to_dict(result['text'])
        print(data)
        # Store the data in a session
        session['data'] = data
        return redirect(url_for('confirmation'))
    else:
        # Return the error message to the user
        return result, 400

# Direct to confirmation page
@app.route('/confirmation')
def confirmation():
    # Retrieve the data from the session
    data = session.get('data')
    return render_template('confirmation.html', data=data)

# Queries the database and returns the JSON data
@app.route('/data', methods=['GET'])
def data():
    data = query_data()
    return jsonify(data)

# Runs the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
