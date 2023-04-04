from flask import Flask, render_template, request, jsonify
from mermaid_to_bugs import translate_v1, translate_v2, generate_mermaid
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/bugs-code/', methods=["POST"])
def my_link():
  user_input = request.form["graph-definition"]
  bugs_code = translate_v2(user_input)
  mermaid_code = generate_mermaid()


  return render_template("index.html", INPUT_NAME_1 = bugs_code, INPUT_NAME_2 = user_input, INPUT_NAME_3 = mermaid_code)

if __name__ == '__main__':
  app.run(debug=True)