from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load existing data from the tracking file
def load_tracking_data():
    try:
        with open('searches.tracked', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to the tracking file
def save_tracking_data(data):
    with open('searches.tracked', 'w') as file:
        json.dump(data, file, indent=4)

# Load existing API credentials
def load_api_credentials():
    try:
        with open('telegram_api_credentials', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save API credentials
def save_api_credentials(data):
    with open('telegram_api_credentials', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    trackings = load_tracking_data()
    api_credentials = load_api_credentials()
    return render_template('index.html', trackings=trackings, api_credentials=api_credentials)

@app.route('/add_tracking', methods=['POST'])
def add_tracking():
    trackings = load_tracking_data()
    name = request.form['name']
    trackings[name] = {
        request.form['url']: {
            request.form['minPrice'] or "null": {
                request.form['maxPrice'] or "null": {}
            }
        }
    }
    save_tracking_data(trackings)
    return redirect(url_for('index'))

@app.route('/delete_tracking/<name>')
def delete_tracking(name):
    trackings = load_tracking_data()
    if name in trackings:
        del trackings[name]
    save_tracking_data(trackings)
    return redirect(url_for('index'))

@app.route('/update_config', methods=['POST'])
def update_config():
    config = {
        'token': request.form['token'],
        'chatId': request.form['chatId']
    }
    save_api_credentials(config)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
