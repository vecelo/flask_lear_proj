from flask import Blueprint, request, render_template, redirect, url_for
from helpers import object_list
from app import db, app
from models import Snippet
from forms import SnippetForm
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

snippets = Blueprint('snippets', __name__, template_folder='templates')

@app.template_filter('pygments')
def pygments_filter(code):
    return highlight(code, PythonLexer(), HtmlFormatter())

@snippets.route('/')
def index():
    snippets = Snippet.query.order_by(Snippet.created_timestamp.desc())
    return object_list('entries/index.html', snippets)

@snippets.route('/<slug>/')
def detail(slug):
    snippet = Snippet.query.filter(Snippet .slug == slug).first_or_404()
    return render_template('snippets/detail.html', entry=snippet)

@snippets.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = SnippetForm(request.form)
        if form.validate():
            snippet = form.save_entry(Snippet())
            db.session.add(snippet)
            db.session.commit()
            return redirect(url_for('snippets.detail', slug=snippet.slug))
    else:
        form = SnippetForm()
    return render_template('snippets/create.html', form=form)

@snippets.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    snippet = Snippet.query.filter(Snippet.slug == slug).first_or_404()
    if request.method == 'POST':
        form = SnippetForm(request.form, obj=snippet)
        if form.validate():
            snippet = form.save_entry(snippet)
            db.session.add(snippet)
            db.session.commit()
        return redirect(url_for('snippets.detail', slug=entry.slug))
    else:
        form = EntryForm(obj=entry)
        
    return render_template('entries/edit.html', entry=snippet, form=form)
