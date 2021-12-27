import json
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def online_page():
    with open('settings.json') as f:
        settings = json.load(f)
    return render_template('index.html', settings=settings)


@app.route('/candidate/<int:id>')
def candidate_page(id):
    with open('candidates.json', encoding="utf-8") as f:
        candidates = json.load(f)
    for candidate in candidates:
        if candidate['id'] == id:
            return render_template('candidate.html', candidate=candidate)


@app.route("/list")
def list_page():
    with open('candidates.json') as f:
        candidates = json.load(f)
    return render_template('list.html', candidates=candidates)


@app.route("/search/")
def search_page():
    name = request.args.get('name')
    with open('candidates.json') as f:
        candidates = json.load(f)
    users = []
    count = len(users)
    if name:
        for candidate in candidates:
            if name == candidate['name']:
                users.append(candidate['name'])
    return render_template('users.html', name=name, count=len(users), users=users)


@app.route("/skill/<x>")
def skills(skill):
    skill = request.args.get('skill')
    with open('settings.json') as f:
        settings = json.load(f)
    with open('candidates.json') as f:
        candidates = json.load(f)
    users = []
    search_limit = 0
    count = len(users)
    for candidate in candidates:
        if skill.lower in candidate['skills']:
            users.append(candidate['name'])
            search_limit += 1
            if settings['limit'] == search_limit:
                return render_template('skill.html', count=count, users=users, search_limit=search_limit)
    return render_template('skill.html', count=count, users=users, search_limit=search_limit)


app.run()
