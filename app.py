from flask import Flask, render_template as render, request, make_response, redirect
from base64 import urlsafe_b64encode as encode, urlsafe_b64decode as decode, b64encode, standard_b64encode
from bz2 import compress, decompress
import marshal

app = Flask(__name__)

@app.after_request
def allow_cross_origin_requests(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/")
def home():
    return render("home.html")

@app.route("/pack", methods=["POST"])
def pack():
    content_type = request.form.get('content-type', 'text/plain')
    body = request.form.get('body', '')

    payload = marshal.dumps(dict(
        body=body,
        content_type=content_type
    ))
    payload = encode(compress(payload))

    return redirect("/%s" % payload)

@app.route("/<data>")
def unpack(data):
    data = marshal.loads(decompress(decode(str(data))))
    resp = make_response(data['body'])
    resp.headers['content-type'] = data['content_type']

    return resp

if __name__=='__main__':
    app.run(debug=True)
