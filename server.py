from flask import Flask, render_template, request, jsonify
from mermaid_to_bugs import translate
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/bugs-code/', methods=["POST"])
def my_link():
  dict = request.form
  for key in dict:
    print(key)
    print (dict[key])
  bugs_code = translate()

  return render_template("index.html", INPUT_NAME_1 = bugs_code)

if __name__ == '__main__':
  app.run(debug=True)