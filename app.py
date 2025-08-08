import os
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
import yaml


app = Flask(__name__)
app.secret_key='secret1'

# Helper functions
def get_data_dir():
    subdir = 'tests/data' if app.config['TESTING'] else 'flashcards/data'
    return os.path.join(os.path.dirname(__file__), subdir)

# Route hooks
@app.route('/')
def index():
    data_dir = get_data_dir()
    decks = [os.path.basename(path) for path in os.listdir(data_dir)]

    return render_template('flashcards.html', decks=decks)

@app.route('/deck/<deckname>')
def display_deck(deckname):
    data_dir = get_data_dir()
    deck_dir = os.path.join(data_dir, deckname)
    deck_file = os.path.join(deck_dir, 'cards.yml')

    with open(deck_file, 'r', encoding='utf-8') as f:
        deck_data = yaml.safe_load(f)

    cards = deck_data.get('cards', [])
    deck_title = deck_data.get('name', deckname)

    return render_template('deck.html', deck=cards, deck_title=deck_title)

if __name__ == "__main__":
    app.run(debug=True, port=8080)