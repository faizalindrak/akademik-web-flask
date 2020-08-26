from flask import Flask,redirect,url_for,render_template

app = Flask(__name__)

@app.route("/user/<names>")
def home(names):
    return render_template("index.html", content=names)

@app.route("/<name>")
def user(name):
    return f"Hello {name}!" #formating

@app.route("/admin/")
def admin():
    return redirect(url_for("user", name="Admin!")) #redirect

if __name__ == "__main__":
    app.run(debug=True)