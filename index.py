from flask import *
import sqlite3
import os

app = Flask(__name__)

app.secret_key="aniketmore"




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/register")
def hello():
    return render_template("registration.html")


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        fn = request.form["full_name"]
        dob = request.form["dob"]
        pn = request.form["phone"]
        gr = request.form.get("Guardian")
        em = request.form["email"]
        ps = request.form["password"]
        cps = request.form["confirm_password"]
        street = request.form["street"]
        ci = request.form["city"]
        st = request.form["state"]
        pin = request.form["pin"]
        country = request.form["country"]
        ed = request.form["education"]
        fi = ','.join(request.form.getlist("fid"))
        at = request.form["acc_type"]
        ac = request.form["acc_cate"]
        dp = request.form["deposite"]



        con = sqlite3.connect("BankSystem2.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (Fullname, DoB, MobileNo, Guardian ,email, password, Confirm_password,street_address, city, state, pincode, country, Education, Identification,Account_type, Account_category, deposite) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [fn, dob, pn, gr, em, ps, cps, street, ci, st, pin, country, ed, fi, at, ac, dp])
        con.commit()
        con.close()
        return redirect(url_for("login"))

    else:
        return render_template("registration.html")




#  Login fronted

@app.route("/login") # frontend
def login():
     return render_template("login.html")

# Login Backend

@app.route("/checklogin", methods=["POST", "GET"])
def checklogin():
    if request.method == "POST":
        em = request.form['email']
        ps = request.form['password']

        con = sqlite3.connect("BankSystem2.db")
        cur = con.cursor()
        cur.execute("select * from users WHERE email=? AND password=?", [em, ps])

        data = cur.fetchall()
        con.close()

        if len(data) == 1:
            session["username"] = em  # session start
            return "<script>window.alert('Login Succesfully'); window.location.href='/dashboard'</script>"

        else:
            return "<script>window.alert('Login Fails'); window.location.href='/login'</script>"





@app.route("/admin")
def admin():
    if "username" not in session:
        return redirect(url_for("index"))

    return render_template("admin.html")


@app.route("/checking", methods=['GET', 'POST'],endpoint='checking')
def admincheck():
        admin_username = 'admin'
        admin_password = '123'
        

        session["username"] =  admin_username

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            

            if username == admin_username and password == admin_password:
                 
                return "<script>window.alert('LOGIN SUCCESFULL !'); window.location.href='/admin'</script>"
            else:
                return "<script>window.alert('Invalid credentials. Please try again.'); window.location.href='/adminlogin'</script>"


        return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    con = sqlite3.connect("BankSystem2.db")
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template("Dashboard.html",data=data)



@app.route("/logout")
def logout():
    session.pop("username",None) # session closed on dashbord
    return redirect(url_for('login'))



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact",methods=["POST","GET"])
def contactpage():
    if request.method == "POST":
        nm=request.form["name"]
        em=request.form["email"]
        ph=request.form["phone"]
        sub=request.form["subject"]
        mes=request.form["message"]

        con = sqlite3.connect("BankSystem2.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO contact (name,email,phone,subject,message) VALUES (?, ?, ?, ?, ?)",
            [nm,em,ph,sub,mes])
        con.commit()
        con.close()
        return "<script>window.alert('Thank you for Contact us..!'); window.location.href='/home'</script>"
        #return redirect(url_for("index"))

    else:
        return "<script>window.alert('Sorry Fails to Contact Us plz Try again'); window.location.href='/home'</script>"
        #return render_template("contact.html")




@app.route("/loans")
def loans():
    return render_template("loan.html")


@app.route("/loan",methods=["POST","GET"])
def loan():
    if request.method == "POST":
        nm=request.form["name"]
        em=request.form["email"]
        phn = request.form["phone"]
        am=request.form["amount"]
        lty = request.form["loan-type"]
        ten = request.form["tenure"]

        con = sqlite3.connect("BankSystem2.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO loans (fullname,email,phonenumber,loanamount,loantype,loantenure,status) VALUES (?, ?, ?, ?,?,?,'Pending')",
            [nm,em,phn,am,lty,ten])
        con.commit()
        con.close()

        return "<script>window.alert('Loan Application Submitted'); window.location.href='/dashboard'</script>"
        # return redirect(url_for("index"))

    else:
        return "<script>window.alert('Sorry Fails to Apply plz Try again'); window.location.href='/dashboard'</script>"
        # return render_template("contact.html")







@app.route("/apply")
def apply():
    return render_template("applyloan.html")

@app.route("/reset")
def reset():
    return render_template("resetpass.html")

@app.route("/support1")
def support1():
    return render_template("support.html")

@app.route("/transaction")
def transaction():
    return render_template("transaction.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/setting")
def setting():
    return render_template("settings.html")

@app.route("/userprofile")
def userprofile():

    if session.get("username") is not None:
        con = sqlite3.connect("BankSystem2.db")
        cur = con.cursor()
        cur.execute("select * from users where email=?", [session.get("username")])
        data = cur.fetchall()
        con.close()
        return render_template("user_profile.html", data=data)
    else:
        return redirect(url_for("login"))


    #return render_template("user_profile.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")



# show database
@app.route("/showdata")
def showdata():
    con = sqlite3.connect("BankSystem2.db")
    cur = con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()


    return render_template("showdata.html",data=data)

@app.route("/manage")
def manage():
    con = sqlite3.connect("BankSystem2.db")
    cur = con.cursor()
    cur.execute("select id,Fullname,email,MobileNo,DoB,Identification from users")
    data=cur.fetchall()


    return render_template("manageacc.html",data=data)

@app.route("/pending", methods=["GET", "POST"])
def pending():
    con = sqlite3.connect("BankSystem2.db")
    cur = con.cursor()
    if request.method == "POST":
        loan_id = request.form.get("loan_id")
        action = request.form.get("action")

        if loan_id and action == "approve":
            cur.execute("UPDATE loans SET status='Approved' WHERE id=?", (loan_id,))
            con.commit()
        elif loan_id and action == "reject":
            cur.execute("UPDATE loans SET status='Rejected' WHERE id=?", (loan_id,))
            con.commit()

    cur.execute("SELECT * FROM loans")
    data = cur.fetchall()
    con.close()
    return render_template("approvals.html", data=data)

#delete Accounts (Admin Dashboard)
@app.route("/deleteaccount/<int:id>", methods=["POST"])
def delete(id):
    con = sqlite3.connect("BankSystem2.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id=?", [id])
    con.commit()
    con.close()

    return  "<script>window.alert('Account deleted Sucessfully'); window.location.href='/manage'</script>"

#Complaints and Feedbacks(Admin Dashboard)
@app.route("/complaint")
def complaint():
    con = sqlite3.connect('BankSystem2.db')
    cur = con.cursor()
    cur.execute("select * from support")
    data = cur.fetchall()
    con.commit()

    return render_template("complaints.html",data=data)

#Complaints or Support (User Dashobard)
@app.route("/support",methods=["POST","GET"])
def support():
    if request.method=="POST":
        fn = request.form["fullname"]
        em = request.form["email"]
        su = request.form["subject"]
        ms = request.form["message"]

    con = sqlite3.connect("BankSystem2.db")
    cur = con.cursor()
    cur.execute("insert into support(fullname, email, subject,message) values(?,?,?,?)",[fn,em,su,ms])
    con.commit()
    con.close()

    return "<script>window.alert('Sorry for Inconvenient..! If any issue we will solve as soon as possible'); window.location.href='/dashboard'</script>"


# loan database(Admin Dashboard)
@app.route("/loandatabse")
def loandb():
    con = sqlite3.connect("BankSystem2.db")
    cur = con.cursor()
    cur.execute("select id,fullname,email,phonenumber,loanamount,loantype,loantenure from loans ")
    data=cur.fetchall()


    return render_template("loandatbase.html",data=data)



if __name__=='__main__':
    app.run(debug=True)