from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Proposal
import os

app = Flask(__name__)

# 使用環境變數設定 secret_key
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")

# SQLite 也在這裡設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            flash('User already exists!')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('proposals'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/proposals', methods=['GET', 'POST'])
@login_required
def proposals():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        p = Proposal(title=title, description=desc)
        db.session.add(p)
        db.session.commit()
        flash('Proposal added.')
        return redirect(url_for('proposals'))
    
    all_proposals = Proposal.query.all()
    users = User.query.all()
    users_dict = {u.id: u.username for u in users}
    return render_template('proposals.html', proposals=all_proposals, current_user=current_user, users_dict=users_dict)

    
    # 顯示所有提案
    all_proposals = Proposal.query.all()
    return render_template('proposals.html', proposals=all_proposals, current_user=current_user)

@app.route('/claim/<int:proposal_id>')
@login_required
def claim(proposal_id):
    proposal = Proposal.query.get_or_404(proposal_id)
    if proposal.claimed_by is None:
        proposal.claimed_by = current_user.id
        db.session.commit()
        flash('You have claimed the proposal!')
    else:
        flash('Proposal already claimed.')
    return redirect(url_for('proposals'))

@app.route('/dashboard')
@login_required
def dashboard():
    users = User.query.all()
    data = []
    for user in users:
        total_claimed = Proposal.query.filter_by(claimed_by=user.id).count()
        total_completed = Proposal.query.filter_by(claimed_by=user.id, status='completed').count()
        data.append({'username': user.username, 'claimed': total_claimed, 'completed': total_completed})
    return render_template('dashboard.html', data=data)

@app.route('/complete/<int:proposal_id>')
@login_required
def complete(proposal_id):
    proposal = Proposal.query.get_or_404(proposal_id)
    if proposal.claimed_by == current_user.id:
        proposal.status = 'completed'
        db.session.commit()
        flash('Proposal marked as completed.')
    else:
        flash('You cannot complete this proposal.')
    return redirect(url_for('proposals'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


'''
| 欄位名稱                            | 說明                                                               | 如何取得                     |
| ------------------------------- | ---------------------------------------------------------------- | ------------------------ |
| `"type"`                        | 固定為 `"service_account"`                                          | 系統自動填入                   |
| `"project_id"`                  | 你的 Google Cloud 專案 ID（例如：`my-gcp-project-123`）                   | GCP 控制台首頁 / 左上方導航列       |
| `"private_key_id"`              | Google 產生的憑證 ID，用來辨識私鑰                                           | 建立憑證時自動產生                |
| `"private_key"`                 | 你的私密金鑰（PEM 格式，會以多行 `-----BEGIN PRIVATE KEY-----` 開頭）             | 建立憑證時自動產生                |
| `"client_email"`                | 服務帳戶的 Email（例如：`mvp-bot@my-gcp-project.iam.gserviceaccount.com`） | 在 IAM → 服務帳戶 → 點服務帳戶即可看到 |
| `"client_id"`                   | GCP 系統分配的帳戶 ID                                                   | 同上，會出現在 JSON 檔           |
| `"auth_uri"`                    | 固定為 `https://accounts.google.com/o/oauth2/auth`                  | 標準 Google 認證網址           |
| `"token_uri"`                   | 固定為 `https://oauth2.googleapis.com/token`                        | 標準 Google token API      |
| `"auth_provider_x509_cert_url"` | 固定為 Google 的憑證 URL                                               | 標準值                      |
| `"client_x509_cert_url"`        | 對應該服務帳戶的公開憑證 URL                                                 | 自動生成，通常不需修改              |


📥 如何下載 JSON 憑證
登入 Google Cloud Console
選擇你要的專案
點左側「IAM 與管理」>「服務帳戶」
建立新的服務帳戶，或點進現有服務帳戶
點「金鑰」頁籤 → 點「新增金鑰」
選擇「JSON」格式並下載
✅ 這時你就會拿到含上述所有欄位的 .json 檔案！
'''
