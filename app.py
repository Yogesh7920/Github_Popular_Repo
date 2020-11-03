from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)


def github(org, n, m):
    repos = requests.get('https://api.github.com/orgs/ORG/repos', {'org': org})
    repos = repos.json()
    repos = sorted(repos, key=lambda x: x.get('forks', 0), reverse=True)[:n]
    result = []
    for repo in repos:
        contrib_url = repo.get('contributors_url')
        print(contrib_url)
        contrib = requests.get(contrib_url)
        if contrib.status_code == 200:
            contrib = contrib.json()
            contrib = contrib[:m]
            contrib = list(map(lambda x: {
                'name': x['login'],
                'contributions': x['contributions']
            }, contrib))

            result.append({
                'name': repo['name'],
                'contributors': contrib,
                'fork_count': repo.get('forks', 0)
            })

    return result


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        org = request.form['org']
        m = int(request.form['M'])
        n = int(request.form['N'])
        results = github(org, m, n)
        return render_template('result.html', results=results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
