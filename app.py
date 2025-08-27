from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Database configuration (SQLite file named notes.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

# Home page (show all notes)
@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)

# Add new note
@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("note")  # get input field from form
    if text:  # make sure it's not empty
        new_note = Note(text=text)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for("home"))

# Delete a note
@app.route("/delete/<int:note_id>")
def delete(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for("home"))

# Clear the table
@app.route("/clear", methods = ["POST"])
def clear():
    db.session.query(Note).delete()
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create table if not exists
    app.run(host="0.0.0.0", port=5000, debug=True)
