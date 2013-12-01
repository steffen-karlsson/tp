from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/ajax/review/', methods=['POST'])
def get_review_page_information():
    test = "aaa"
    if request.method == "POST":
        if request.form.get('url', False):
            test = request.form.get('url', 'False')
        else:
            test = 'abc1'
    return jsonify(rma_score=25, price_score=50, delivery_score=75, general_score=100)

@app.route('/')
def index():
    return render_template('index.html')
