from flask import Flask, render_template, abort, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlalchemy
from flask_mail import Mail, Message
import os
from config import mail_username, mail_password
from flask_share import Share

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SECRET_KEY']= os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = "smtp.googlemail.com'"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password


mail = Mail(app),

db = SQLAlchemy(app)

admin = Admin(app)


class Posts(db.Model):
    __tablename__ = "Blogpost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime)
    slug = db.Column(db.String(255))
    
    def __init__(self, title, subtitle, author, date_posted, content, slug):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.date_posted = date_posted
        self.content = content
        self.slug = slug


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


admin.add_view(SecureModelView(Posts, db.session))


@app.route("/")
def homepage():
    
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")
@app.route("/conflict")
def conflict():
    return render_template("conflict.html")
@app.route("/displacement")
def displacement():
    return render_template("displacement.html")
@app.route("/landuse")
def landuse():
    return render_template("landuse.html")

@app.route('/blog')
def blog():
    posts = Posts.query.order_by(Posts.date_posted.desc()).all()

    return render_template('blog.html', posts=posts)

@app.route("/post/<string:slug>")
def post(slug):
    try:
        post = Posts.query.filter_by(slug=slug).one()
        return render_template("post.html", post=post)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        msg = Message(
            subject=f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\nPhone: {phone}\n\n\n{message}", sender=mail_username, recipients=['yourpersonalemail@protonmail.com'])
        mail.send(msg)
        return render_template("contact.html", success=True)

    return render_template("contact.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == os.environ["username"] and request.form.get("password") == os.environ["password"]:
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed=True)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/ads")
def ads():
    return render_template("ads.txt")

if __name__ == "__main__":
    app.run(debug=True)
