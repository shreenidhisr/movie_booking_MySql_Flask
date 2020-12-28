import pymysql

db = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Sd@8050102193",
    db="movie_db",
    autocommit=True,
)

cur = db.cursor()


def add_admin(name, password):
    sql = "insert into `admin`(`name`,`password`) values(%s,%s)"
    cur.execute(sql, (name, password))
    # row = cur.fetchall()
    # for r in row:
    #     print(r)
    print("ok")


def get_admin():
    sql = "select * from admin"
    cur.execute(sql)
    return cur.fetchall()


def add_user(name, phno, email, password):
    sql = (
        "insert into `visitor`(`v_name`,`phno`,`email`,`password`) values(%s,%s,%s,%s)"
    )
    cur.execute(sql, (name, phno, email, password))
    print("ok")


def get_user():
    sql = "select * from visitor"
    cur.execute(sql)
    return cur.fetchall()


def delete_user(name):
    sql = "delete from visitor where v_name=%s"
    cur.execute(sql, (name))
    print("ok")


def add_movie(name, release_date, language, synopsis):
    sql = (
        "insert into movie(m_name,m_release,m_language,m_synopsis) values (%s,%s,%s,%s)"
    )
    cur.execute(sql, (name, release_date, language, synopsis))
    print("ok")


def update_movie(name, release_date, language, synopsis):
    sql = "update movie set m_release=%s,m_language=%s,m_synopsis=%s where m_name=%s"
    cur.execute(sql, (release_date, language, synopsis, name))
    print("ok")


def delete_movie(name):
    sql = "delete from movie where m_name=%s"
    cur.execute(sql, (name))
    print("ok")


def get_movies():
    sql = "select m_name from movie"
    cur.execute(sql)
    result = cur.fetchall()
    return result


def get_movies_filetered(name):
    sql = "select * from movie where m_name like %s"
    m_name = "%" + name + "%"
    cur.execute(sql, m_name)
    return cur.fetchall()


def add_venue(capacity, name):
    sql = "insert into venue(v_capacity,v_name) values(%s,%s)"
    cur.execute(sql, (capacity, name))
    print("ok")


def update_venue(capacity, name):
    sql = "update venue set v_capacity=%s"
    cur.execute(sql, (capacity))
    print("ok")


def get_all_movies():
    sql = "select * from movie"
    cur.execute(sql)
    return cur.fetchall()


def delete_venue(name):
    sql = "delete from venue where v_name=%s"
    cur.execute(sql, name)
    print("ok")


def get_venues():
    sql = "select v_name from venue"
    cur.execute(sql)
    result = cur.fetchall()
    return result


def book_ticket(
    no_ticket, m_name, show_no, m_date, v_name, vis_email, amount, payment_id
):
    sql1 = "insert into book_ticket((no_ticket,m_name,show_no,m_date,v_name,vis_email)values(%s,%s,%s,%s,%s,%s)"
    sql2 = "insert into payment(v_email,amount,payment_id)values(%s,%s,%s)"
    cur.execute(sql1, (no_ticket, m_name, show_no, m_date, v_name, vis_email))
    cur.execute(sql2, (vis_email, amount, payment_id))
