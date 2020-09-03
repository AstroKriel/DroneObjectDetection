from flask import Flask, request, render_template
import json
app = Flask(__name__)

Shared_data = {"Test":"test"}

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/data', methods=['GET','POST'])
def test():
    global Shared_data
    if request.method == "POST":
        data = request.data
        parsed_data = json.loads(data)
        print(parsed_data)
        Shared_data.clear()
        Shared_data = parsed_data
        return json.dumps(parsed_data)
    else:
        return render_template('data.html', data=Shared_data)

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
    """
    CURL Test command:
    curl -X POST -H "Content-Type: application/json" -d {\"username\":\"abc\",\"password\":\"abc\"} http://192.168.43.146:5000/data
    """