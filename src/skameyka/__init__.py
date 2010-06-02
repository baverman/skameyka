from flask import Flask, json, render_template, Response, request

from taburetkit import Client
from .ui import make_object_decoder

app = Flask('skameyka')
app.secret_key = 'lkjhasd;fhas,mbnzxclkjvasldfgasdmbvwekarhgwqer'

client = Client('http://localhost:5000')

decoder = make_object_decoder(client)

@app.route('/')
def index():
    data = client.invoke('/accounting/form/accounts-plan')
    form = decoder.decode(json.loads(data))
    return render_template('form.html', form=form)
   
@app.route('/taburet/<path:path>', methods=('POST', 'GET'))
@app.route('/taburet/', methods=('POST', 'GET'))
def taburet_endpoint(path=''):
    result = client.invoke('/' + path, request.args.items()) #@UndefinedVariable
    return Response(result, mimetype='application/json')