from flask import Flask, render_template, request, jsonify
from mermaid_to_bugs import translate
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/bugs-code/', methods=["POST"])
def my_link():
  mermaid_code = request.form["graph-definition"]
  bugs_code = translate(mermaid_code)

  return render_template("index.html", INPUT_NAME_1 = bugs_code, INPUT_NAME_2 = mermaid_code)

if __name__ == '__main__':
  app.run(debug=True)