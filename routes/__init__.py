from flask import Blueprint

# 為了確保 blueprint 註冊順利
auth = Blueprint('auth', __name__)
proposal_routes = Blueprint('proposal', __name__)
dashboard = Blueprint('dashboard', __name__)
