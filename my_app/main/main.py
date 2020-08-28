from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/<name>')
def index(name=''):
    return render_template('index.html', name=name)
