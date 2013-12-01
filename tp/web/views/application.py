from flask import Flask, jsonify, render_template
app = Flask(__name__)

@app.route('/ajax/review/')
def get_review_page_information():
    return jsonify(result='test')

@app.route('/')
def index():
    return render_template('index.html')
