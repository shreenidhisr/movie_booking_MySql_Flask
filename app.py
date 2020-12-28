from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    redirect,
    url_for,
    jsonify,
    flash,
)

from functools import wraps
from forms import signinForm, loginForm
from db import *
import os
import random
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if EMAIL_ID:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("loginpage"))

    return wrap


app = Flask(__name__)
app.config["SECRET_KEY"] = "hehhhGWGg"
app.config[
    "UPLOAD_FOLDER"
] = "C:\\Users\\asus\\Desktop\\webdev\\flask_app\\static\\images"
app.config["MAIL_SERVER"] = ("smtp.gmail.com",)
app.config["MAIL_PORT"] = (465,)
app.config["MAIL_USE_SSL"] = (True,)
app.config["MAIL_USERNAME"] = ("testshreenidhi@gmail.com",)
app.config["MAIL_PASSWORD"] = "8050102193"
mail = Mail(app)


# GLOBAL VARIABLES
mov = ""
ROW_ID = 0
USER = "User"
MSG = "Welcome Admin"
MOVIE = ""
VENUE = ""
SHOW_NO = ""
NO_OF_TICKETS = 0
DATE = ""
EMAIL_ID = ""
TID = 0
AMOUNT = 0


@app.route("/", methods=["GET", "POST"])
def loginpage():
    form = loginForm()
    if form.validate_on_submit():
        print("validated")
        email = form.email.data
        password = form.password.data
        print(email, password)

        for admin in get_admin():
            if email == admin[2] and password == admin[3]:
                print("admin here")
                global USER, EMAIL_ID
                USER = "ADMIN"
                EMAIL_ID = email
                return redirect("/adminDashboard/")
            else:
                flag = False

        for user in get_user():
            if email == user[3] and password == user[4]:
                flag = True
                EMAIL_ID = email
                USER = user[1]
                break
            else:
                flag = False
        if flag == True:
            return redirect("/showmovies/")
        else:
            flash("Wrong user credentials!Please sign in to continue")
            return redirect("/")

    return render_template("login.html", form=form)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = signinForm()
    if form.validate_on_submit():
        print("inside")
        name = form.name.data
        email = form.email.data
        phno = form.phno.data
        password = form.password.data
        cur.execute("select email from visitor")
        emails1 = [item[0] for item in cur.fetchall()]
        print(emails1)
        if email in emails1:
            print("true")
            flash("Email id already exist!Please use another mail")
            return redirect(url_for("signin"))

        add_user(name, phno, email, password)
        print(name, email, password)
        return redirect(url_for("loginpage"))
    return render_template("signin.html", form=form)


@app.route("/showmovies/")
@login_required
def showmovies():
    rows = get_all_movies()
    print(rows)
    return render_template("movies.html", USER=USER, rows=rows)


@app.route("/adminDashboard/showmovies/")
@login_required
def showadminmovies():
    rows = get_all_movies()
    print(rows)
    return render_template("adminmovies.html", USER=USER, rows=rows)


@app.route("/searchMovie", methods=["GET", "POST"])
@login_required
def searchMovie():
    if request.method == "POST":
        search = request.form["search_data"]
        rows = get_movies_filetered(search)
        return render_template("movies.html", USER=USER, rows=rows)
    return redirect(url_for("/showmovies/"))


@app.route("/logout")
@login_required
def logout():
    global EMAIL_ID
    EMAIL_ID = ""
    flash("logged out succesfully")
    return redirect(url_for("loginpage"))


@app.route("/showBookTickets")
@app.route("/showmovies/showBookTickets/")
@login_required
def showBookTickets():
    mnames = get_movies()
    vnames = get_venues()
    return render_template("tickets.html", USER=USER, mnames=mnames, vnames=vnames)


@app.route("/checkAvail", methods=["POST", "GET"])
@login_required
def availability():
    flag = False
    print("INSIDE")
    if request.method == "POST":
        movie = request.form["movie"]
        venue = request.form["venue"]
        show_no = request.form["show_no"]
        no_of_tickets = request.form["no_of_tickets"]
        date = request.form["date"]
        movie = movie[2:-3].strip()
        venue = venue[2:-3].strip()
        global MOVIE, VENUE, SHOW_NO, NO_OF_TICKETS, DATE
        MOVIE = movie
        VENUE = venue
        SHOW_NO = show_no
        NO_OF_TICKETS = no_of_tickets
        DATE = date
        cur.execute("select v_capacity from venue where v_name=%s", (venue,))
        v_capacity = str(cur.fetchall())
        print(v_capacity)
        no = int(v_capacity[2:-4])
        print(no)
        try:
            cur.execute(
                "select no_of_ticket from book_ticket where m_name = %s and v_name = %s and show_no = %s and m_date = %s",
                (movie, venue, show_no, date),
            )
            seatsAvailable = cur.fetchone()
        finally:
            seatsAvailable = 0

        print(seatsAvailable)
        if no > seatsAvailable:
            return redirect("/payment/")
        else:
            return render_template("tickets.html")

    if flag == True:
        return redirect("/showmovies/")
    else:
        return redirect("/")


@app.route("/showAboutUs")
@login_required
def showAboutUs():
    return render_template("aboutUs.html")


@app.route("/payment/")
@login_required
def pay():
    global NO_OF_TICKETS, USER, MOVIE, VENUE, SHOW_NO, NO_OF_TICKETS, DATE, EMAIL_ID, AMOUNT, TID
    cost = int(NO_OF_TICKETS) * 100
    AMOUNT = cost
    tid = random.randint(1, 1000)
    TID = tid
    return render_template(
        "payment.html",
        cost=cost,
        user=USER,
        movie=MOVIE,
        venue=VENUE,
        show_no=SHOW_NO,
        tickets=NO_OF_TICKETS,
        date=DATE,
        email=EMAIL_ID,
        tid=tid,
    )


@app.route("/book", methods=["POST", "GET"])
@login_required
def book():
    flag = False
    print("INSIDE")
    if request.method == "POST":
        global MOVIE, VENUE, SHOW_NO, NO_OF_TICKETS, DATE, EMAIL_ID, TID, AMOUNT
        print(MOVIE)
        print(VENUE)
        print(SHOW_NO)
        print(NO_OF_TICKETS)
        print(DATE)
        print(EMAIL_ID)
        print(TID)
        print(AMOUNT)
        cur.execute(
            "INSERT INTO BOOK_TICKET(no_of_ticket, m_name, show_no, m_date,v_name, vis_email) VALUES (%s,%s,%s,%s,%s,%s)",
            (NO_OF_TICKETS, MOVIE, SHOW_NO, DATE, VENUE, EMAIL_ID),
        )
        print("insert into book_ticket success")
        cur.execute(
            "INSERT INTO PAYMENT(v_email,amount,m_name,payment_id) VALUES (%s,%s,%s,%s)",
            (EMAIL_ID, AMOUNT, MOVIE, TID),
        )
        cur.execute(
            "update venue set v_capacity=v_capacity-%s where v_name=%s",
            (NO_OF_TICKETS, VENUE),
        )
        print("insert into PAYMENT success")
        flag = True

        # msg = Message("Hello", sender="testshreenidhi@gmail.com", recipients=[EMAIL_ID])
        # msg.body = "Hello Flask message sent from Flask-Mail"
        # mail.send(msg)

    if flag == True:
        return redirect(url_for("showmovies"))
    else:
        return redirect(url_for("showmovies"))


@app.route("/viewProfile")
@login_required
def profile():
    cur.execute("select * from visitor where email=%s", (EMAIL_ID))
    print(EMAIL_ID)
    rows = cur.fetchone()
    print(rows)
    return render_template("profile.html", rows=rows)


# admin functionalities


@app.route("/adminDashboard/")
@login_required
def adminDashboard():
    global MSG
    return render_template("admin.html", MSG=MSG)


@app.route("/adminDashboard/addMovie/")
@login_required
def showaddMovie():
    return render_template("addmovie.html")


@app.route("/history")
@login_required
def history():
    # user=EMAIL_ID
    cur.execute("select * from book_ticket where vis_email=%s", (EMAIL_ID))
    r = cur.fetchall()
    return render_template("history.html", rows=r)


@app.route("/addmovie", methods=["POST", "GET"])
@login_required
def addmovie():
    flag = False
    if request.method == "POST":
        try:
            name = request.form["name"]
            # rating = request.form["rating"]
            release = request.form["release"]
            language = request.form["language"]
            synopsis = request.form["synopsis"]
            f = request.files["image"]
            f.save(
                os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename))
            )
            print("A")

            if not name or not release or not language or not synopsis:
                print("B")
                return render_template("addmovie.html")
            else:
                print("C")
                cur.execute(
                    "INSERT INTO movie (m_name,m_release,m_language,m_synopsis,image_path) VALUES (%s,%s,%s,%s,%s)",
                    (name, release, language, synopsis, secure_filename(f.filename)),
                )
                flag = True

        except:

            db.rollback()
        finally:
            if flag == True:
                return redirect("/adminDashboard/")
            else:
                flash("Can't add your movie.")
                return redirect("/adminDashboard/")


@app.route("/removeMovie/")
@app.route("/adminDashboard/removeMovie/")
@login_required
def showremoveMovie():
    cur.execute("select m_name from movie")
    mnames = cur.fetchall()
    return render_template("removeMovie.html", mnames=mnames)


@app.route("/removeMovie", methods=["POST", "GET"])
@login_required
def removemovie():
    flag = False
    print("outside")
    if request.method == "POST":
        try:
            name = request.form["movie"]
            print(name)

            name = name[2:-3].strip()
            name = name
            print("BEFORE QUERY")
            cur.execute("DELETE FROM movie WHERE m_name= %s", (name,))
            print("afTER  QUERY")
            flag = True

        except:
            db.rollback()
        finally:
            if flag == True:
                return redirect("/adminDashboard/")
            else:
                flash("can't remove movie")
                return redirect("/removeMovie/")


@app.route("/adminDashboard/updateMovie/")
@login_required
def updateMovie():
    cur.execute("select m_name from movie")
    mnames = cur.fetchall()
    return render_template("updateMovie.html", mnames=mnames)


@app.route("/updateMovie2", methods=["POST", "GET"])
@login_required
def updatemovie():
    flag = False
    print("outside")
    if request.method == "POST":
        name = request.form["movie"]

        print(name)
        name = name[2:-3].strip()
        name = name
        mov = name
        print("BEFORE QUERY")
        cur.execute("select * from movie where m_name=%s", (name))
        result = cur.fetchall()
        return render_template("updateTemplate.html", mnames=result)


@app.route("/updateMovieDetails", methods=["POST", "GET"])
@login_required
def updMovie():
    flag = False
    print("outside")
    if request.method == "POST":
        name = request.form["m_name"]
        release = request.form["m_release"]
        lang = request.form["m_language"]
        synopsis = request.form["m_synopsis"]
        print(name)
        print(mov)

        cur.execute(
            "update movie set m_name=%s,m_release=%s,m_language=%s,m_synopsis=%s where m_name=%s",
            (name, release, lang, synopsis, name),
        )
        return redirect("/adminDashboard/")


if __name__ == "__main__":
    app.run(debug=True)