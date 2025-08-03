from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.models import db, User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("請輸入帳號和密碼")
            return render_template("login.html")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard.show_dashboard"))
        flash("Invalid username or password")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        county = request.form.get("county")
        town = request.form.get("town")
        village = request.form.get("village")
        if not username or not password or not county or not town or not village:
            flash("請完整填寫所有欄位")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
        else:
            user = User(username=username, county=county, town=town, village=village)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully")
            return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth.route('/api/counties')
def get_counties():
    counties = ["台北市", "新北市"]
    return jsonify(counties)

@auth.route('/api/towns')
def get_towns():
    county = request.args.get('county')
    towns_data = {
        "台北市": ["中正區", "大安區"],
        "新北市": ["板橋區", "新莊區"]
    }
    towns = towns_data.get(county, [])
    return jsonify(towns)

@auth.route('/api/villages')
def get_villages():
    county = request.args.get('county')
    town = request.args.get('town')
    villages_data = {
        "台北市": {
            "中正區": ["仁愛里", "幸福里"],
            "大安區": ["和平里", "新興里"]
        },
        "新北市": {
            "板橋區": ["民生里", "新興里"],
            "新莊區": ["幸福里", "仁愛里"]
        }
    }
    villages = villages_data.get(county, {}).get(town, [])
    return jsonify(villages)
