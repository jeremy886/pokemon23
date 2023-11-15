import random
from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to your own secret key


@app.route('/', methods=['GET', 'POST'])
def index():
    pokemon_data = None
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name').lower().strip()
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
        if response.status_code == 200:
            pokemon_data = response.json()

    return render_template('index.html', pokemon_data=pokemon_data)


@app.route('/share', methods=['GET', 'POST'])
def share():
    pokemon_link = ""
    if request.method == 'POST':
        pokemon_link = request.form.get('pokemon_link').lower().strip()
        with open("pokemon_links.txt", "a") as PFILE:
            PFILE.write(pokemon_link + "\n")

    pokemon_links = open("pokemon_links.txt", "r").readlines()
    return render_template('share.html', pokemon_links=pokemon_links)

@app.route('/hello/<name>', methods=['GET'])
def hello(name):
    return f"""
<div id="welcome-letter" style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 20px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
    <h1 style="color: #333;">Hello {name}!</h1>
    <p style="color: #555;">Welcome to our community where your love for Pokémon is shared and celebrated.</p>
    <p style="color: #555;">Join us in discussing strategies, sharing experiences, and enjoying the world of Pokémon together.</p>
    <p style="color: #555;">Stay connected for the latest updates and fun events.</p>
    <p style="color: #555;">Happy exploring!</p>
    <p style="margin-top: 30px; color: #333;"><strong>Cheers,</strong><br>Hamilton Pokemon Club</p>
    <hr/>
    <a href="/">Home</a> <a href="/share">Share</a>
</div>
"""


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if 'secret_number' not in session:
        session['secret_number'] = random.randint(1, 10)
        session['attempts'] = 0

    message = ""
    if request.method == 'POST':
        guess = int(request.form.get('guess'))
        session['attempts'] += 1

        if guess == session['secret_number']:
            message = f"You guessed it in {session['attempts']} attempts!"
            session.clear()
        elif guess < session['secret_number']:
            message = "Higher!"
        else:
            message = "Lower!"

    return f'''
        <h1>Guess the Number</h1>
        <form method="post">
            <input type="number" name="guess">
            <input type="submit" value="Guess">
        </form>
        <p>{message}</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
