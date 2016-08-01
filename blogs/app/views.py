from flask import request, render_template # render_template la mot function, rat thong dung/extremely common, nen FLASK dung cang nhieu cang tot

from app import app

@app.route('/')
def homepage():
  name = request.args.get('name') # dung de xu ly url http://localhost:5000?name=Hung trong backed, no la GET /?name=Hung
  number = request.args.get('number') # 2 parameter trong 1 url http://localhost:5000/?number=9&name=hung
  if not name:
    name = '<unknow>'
  return render_template('Homepage.html', name = name, number = number)