import json
from flask import Flask, render_template, request
import requests

response = requests.get('candidates.json') #импорт данных в приложение
candidates = response.json()

#settings = json.loads('settings.json') #Импортируйте данные в словарь settings

app = Flask(__name__)

@app.route('/')
def online_page():
    with open('settings.json') as f:
        settings = json.load(f)
    return render_template('index.html', **settings )

@app.route('/candidate/<id>')
def candidate_page(id):
    with open('candidates.json') as f:
        candidates = json.load(f)
    for candidate in candidates:
        if candidate['id'] == id:
            return render_template('candidate.html', **candidate)


@app.route("/list")
def list_page():
    with open('candidates.json') as f:
        candidates = json.load(f)
    return render_template('list.html', **candidates)

@app.route("/search?name=<str:name>/")
def search_page():
    name = request.args.get('name')
    with open('candidates.json') as f:
        candidates = json.load(f)
    users = []
    count = len(users)
    if name:
        for candidate in candidates:
            if name in candidate['name']:
                users.append(candidate['name'])
    return render_template('users.html', name = name, count = count, users = users)

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
                return render_template('skill.html', count = count, users = users, search_limit = search_limit)
    return render_template('skill.html', count=count, users=users, search_limit=search_limit)

app.run()