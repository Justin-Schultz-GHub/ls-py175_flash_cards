import os
import re
from flask import (
                    flash,
                    Flask,
                    render_template,
                    redirect,
                    request,
                    send_from_directory,
                    session,
                    url_for,
                    )
import string
import yaml


app = Flask(__name__)
app.secret_key='secret1'

# Helper functions
def get_data_dir():
    subdir = 'tests/data' if app.config['TESTING'] else 'flashcards/data'
    return os.path.join(os.path.dirname(__file__), subdir)

def deck_exists(path):
    return os.path.exists(path)

def get_deck_path(data_dir, folder_name):
    return os.path.join(data_dir, folder_name)

def generate_next_folder_name(data_dir):
    existing = os.listdir(data_dir)
    pattern = re.compile(r'^deck(\d+)$')
    numbers = []

    for name in existing:
        match = pattern.match(name)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers) + 1 if numbers else 1
    return f'deck{next_number}'

# Route hooks
@app.route('/')
def index():
    data_dir = get_data_dir()
    folders = [os.path.basename(path) for path in os.listdir(data_dir)]
    decks = []

    for folder in folders:
        yaml_path = os.path.join(data_dir, folder, 'cards.yml')
        with open(yaml_path, 'r', encoding='utf-8') as file:
            deck_data = yaml.safe_load(file)

        deck_name = deck_data.get('name', folder)
        decks.append({'folder': folder, 'name': deck_name})

    return render_template('flashcards.html', decks=decks)

@app.route('/deck/<deck_folder>')
def display_deck(deck_folder):
    data_dir = get_data_dir()
    deck_dir = os.path.join(data_dir, deck_folder)
    deck_file = os.path.join(deck_dir, 'cards.yml')

    with open(deck_file, 'r', encoding='utf-8') as f:
        deck_data = yaml.safe_load(f)

    cards = deck_data.get('cards', [])
    deck_title = deck_data.get('name', deck_folder)

    return render_template('deck.html', cards=cards, deck_title=deck_title)

@app.route('/new')
def new_deck():
    return render_template('new_deck.html')

@app.route('/new/create', methods=['POST'])
def create_deck():
    data_dir = get_data_dir()
    deckname = request.form['deckname']

    if not deckname:
        flash('Deck name cannot be empty.', 'error')
        return redirect(url_for('new_deck'))

    deck_folder = generate_next_folder_name(data_dir)
    deck_path = get_deck_path(data_dir, deck_folder)
    os.makedirs(deck_path, exist_ok=False)

    deck_data = {
            'name': deckname,
            'cards': []
        }

    yaml_path = os.path.join(deck_path, 'cards.yml')
    with open(yaml_path, 'w', encoding='utf-8') as file:
        yaml.dump(deck_data, file, allow_unicode=True, default_flow_style=False, sort_keys=False)

    flash(f'Successfully created {deckname}.', 'success')
    return redirect(url_for('index'))

@app.route('/decks/<deck>/rename')
def rename_deck(deck):
    data_dir = get_data_dir()
    deck_path = get_deck_path(data_dir, deck)
    yaml_path = os.path.join(deck_path, 'cards.yml')

    with open(yaml_path, 'r', encoding='utf-8') as file:
        deck_data = yaml.safe_load(file)

    return render_template('rename_deck.html', deck=deck_data, deck_folder=deck)

@app.route('/decks/<deck>', methods=['POST'])
def save_deck(deck):
    data_dir = get_data_dir()
    deck_path = get_deck_path(data_dir, deck)
    yaml_path = os.path.join(deck_path, 'cards.yml')

    with open(yaml_path, 'r', encoding='utf-8') as file:
        deck_data = yaml.safe_load(file)

    new_deck_name = request.form['deckname']

    if not new_deck_name:
        flash('Deck name cannot be empty.', 'error')
        return render_template('rename_deck.html', deck=deck_data, deck_folder=deck)

    deck_data['name'] = new_deck_name

    with open(yaml_path, 'w', encoding='utf-8') as file:
        yaml.dump(deck_data, file, allow_unicode=True, default_flow_style=False)

    flash(f'Deck successfully renamed.', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)