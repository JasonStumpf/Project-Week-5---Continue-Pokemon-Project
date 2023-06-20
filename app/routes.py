from app import app
from .models import Pokemon
from flask import render_template, request
import requests

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pokemon/', methods=['POST'])
def pokemon():
    pokemon_name = request.form['pokemon_name']
    pokemon_data = get_data(pokemon_name)
    return render_template('pokemon.html', data=pokemon_data)

def get_data(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if response.ok:
        pokemon = response.json()
        poke_info = {
            'Name' : pokemon['name'].title(),
            'Ability' : pokemon['abilities'][0]['ability']['name'].title(),
            'Sprite' : pokemon['sprites']['front_default'],
            'HP-Base Stat' : pokemon['stats'][0]['base_stat'],
            'Attack-Base-Stat' : pokemon['stats'][1]['base_stat'],
            'Defense-Base-Stat' : pokemon['stats'][2]['base_stat']
        }
        new_pokemon = Pokemon(
            name=poke_info['Name'],
            ability=poke_info['Ability'],
            hp=poke_info['HP-Base Stat'],
            attack=poke_info['Attack-Base-Stat'],
            defense=poke_info['Defense-Base-Stat']
            )
        new_pokemon.save_poke()
        return poke_info
    
