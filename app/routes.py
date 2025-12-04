from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import db, login_manager
from .models import User, Role, SystemSetting
from .services.crawler import fetch_baidu_news

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.context_processor
def inject_system_settings():
    settings = SystemSetting.query.first()
    return dict(system_settings=settings)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.verify_password(password):
            flash('用户名或密码错误', 'error')
            return redirect(url_for('main.login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))
        
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Backend Management Routes Placeholders

@main.route('/admin/users')
@login_required
def admin_users():
    if current_user.role.name != 'Administrator':
        flash('无权访问', 'error')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@main.route('/admin/roles')
@login_required
def admin_roles():
    if current_user.role.name != 'Administrator':
        flash('无权访问', 'error')
        return redirect(url_for('main.index'))
    roles = Role.query.all()
    return render_template('admin/roles.html', roles=roles)

@main.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if current_user.role.name != 'Administrator':
        flash('无权访问', 'error')
        return redirect(url_for('main.index'))
    
    settings = SystemSetting.query.first()
    if request.method == 'POST':
        settings.app_name = request.form.get('app_name')
        db.session.commit()
        flash('设置已更新', 'success')
        
    return render_template('admin/settings.html', settings=settings)

@main.route('/api/crawl')
@login_required
def api_crawl():
    if not current_user.is_authenticated or current_user.role.name != 'Administrator':
        return jsonify({"error": "unauthorized"}), 403
    kw = request.args.get('kw', '').strip() or request.args.get('q', '').strip() or request.args.get('keyword', '').strip()
    limit = request.args.get('limit', '20')
    pn = request.args.get('pn', '0')
    if not kw:
        return jsonify({"items": [], "kw": kw})
    try:
        items = fetch_baidu_news(kw, limit=int(limit), pn=int(pn))
    except Exception as e:
        return jsonify({"error": str(e), "kw": kw}), 500
    return jsonify({"items": items, "kw": kw})

@main.route('/admin/crawl')
@login_required
def admin_crawl():
    if current_user.role.name != 'Administrator':
        flash('无权访问', 'error')
        return redirect(url_for('main.index'))
    return render_template('admin/crawl.html')
