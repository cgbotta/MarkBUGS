from flask import Flask, render_template, request, redirect
from mermaid_to_bugs import translate_v2, generate_mermaid, clear_all_data
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/bugs-code/', methods=["POST"])
def my_link():
  clear_all_data()
  user_input = request.form["graph-definition"]
  bugs_code = translate_v2(user_input)
  mermaid_code = generate_mermaid()


  return render_template("index.html", INPUT_NAME_1 = bugs_code, INPUT_NAME_2 = user_input, INPUT_NAME_3 = mermaid_code)

@app.route('/clear-data/', methods=["POST"])
def clear():
  clear_all_data()
  return redirect('/')

@app.route('/example/<id>')
def get_example(id):
  clear_all_data()
  file_contents = ""
  try:
    print(id)
    f = open(f'./examples/study_example_{id}.txt', 'r')
    file_contents = f.read()
  except:
    print("error")
  return render_template("index.html", INPUT_NAME_2 = file_contents)


if __name__ == '__main__':
  app.run(debug=True)