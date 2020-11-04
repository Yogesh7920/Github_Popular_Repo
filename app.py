from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)


def github(org, n, m):
    repos = requests.get('https://api.github.com/orgs/ORG/repos', {'org': org})
    if repos.status_code != 200:
        return False
    repos = repos.json()
    repos = sorted(repos, key=lambda x: x.get('forks', 0), reverse=True)[:n]
    result = []
    for repo in repos:
        commits_url = 'https://api.github.com/repos/'+repo.get('full_name')+'/stats/contributors'
        print(commits_url)
        commits = requests.get(commits_url)
        if commits.status_code == 200:
            commits = commits.json()
            commits = sorted(commits, key=lambda x: x['total'], reverse=True)
            commits = commits[:m]
            commits = list(map(lambda x: {
                'name': x['author']['login'],
                'commits': x['total']
            }, commits))

            result.append({
                'name': repo['name'],
                'commits': commits,
                'fork_count': repo.get('forks', 0),
            })

    return result


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        org = request.form['org']
        m = int(request.form['M'])
        n = int(request.form['N'])
        results = github(org, m, n)
        if results:
            return render_template('result.html', results=results, organisation=org, m=m, n=n)
        else:
            return "Failed, Check your internet connection"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
