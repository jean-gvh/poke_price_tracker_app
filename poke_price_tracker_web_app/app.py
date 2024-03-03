from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import PokemonSet, EbaySalesData
import os
from google.cloud import storage
import csv
import functions

# Configuration de l'application Flask
app = Flask(__name__, '/static')

# Configuration de la base de données
DB_USER = 'root'
DB_PASSWORD = 'Tictact0c'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'test'

# Créez une connexion à la base de données MySQL
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine)






@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        selected_image_link = request.form.get('selectedImageLink', '')  # Ajoutez cette ligne
        print(f"Pokemon Name: {pokemon_name}")
        print(f"Selected Image Link: {selected_image_link}")
        # Requête pour obtenir les informations sur les ventes du Pokémon spécifié
        session = Session()
        pokemon_sales = session.query(EbaySalesData).options(joinedload('pokemon_set')).filter(EbaySalesData.card_name == pokemon_name).all()
        session.close()

        # Calcul des KPIs
        num_sales = len(pokemon_sales)
        avg_price = round(sum(sale.card_price_EUR for sale in pokemon_sales) / num_sales, 2) if num_sales > 0 else 0
        max_price = max(sale.card_price_EUR for sale in pokemon_sales) if num_sales > 0 else 0
        min_price = min(sale.card_price_EUR for sale in pokemon_sales) if num_sales > 0 else 0

        kpis = {'num_sales': num_sales, 'avg_price': avg_price, 'max_price': max_price, 'min_price': min_price}

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'pokemon_name': pokemon_name,
                'sales': [{'card_name': sale.card_name, 'card_price_EUR': sale.card_price_EUR, 'sold_date': sale.sold_date, 'seller_ID': sale.seller_ID, 'pokemon_set': {'set_name': sale.pokemon_set.set_name}} for sale in pokemon_sales],
                'kpis': kpis,
                'selectedImageLink': request.form.get('selectedImageLink', '')  # Ajoutez le lien de l'image sélectionnée à la réponse JSON
            })

        return render_template('results.html', pokemon_name=pokemon_name, pokemon_sales=pokemon_sales, kpis=kpis, selectedImageLink=request.form.get('selectedImageLink', ''))

    return render_template('index.html')

@app.route('/autocomplete-pokemon')
def autocomplete_pokemon():
    term = request.args.get('term')  # Récupérer le terme de recherche de la requête AJAX
    suggestions = functions.get_pokemon_suggestions(term)  # Obtenir les suggestions de noms de Pokémon
    return jsonify(suggestions) 

@app.route('/pokemon_details/<pokemon_name>', methods=['GET'])
def pokemon_details(pokemon_name):
    # Requête pour obtenir les informations sur les ventes du Pokémon spécifié
    session = Session()
    pokemon_sales = session.query(EbaySalesData).options(joinedload('pokemon_set')).filter(EbaySalesData.card_name == pokemon_name).all()
    session.close()

    # Calcul des KPIs
    num_sales = len(pokemon_sales)
    avg_price = round(sum(sale.card_price_EUR for sale in pokemon_sales) / num_sales, 2) if num_sales > 0 else 0
    max_price = max(sale.card_price_EUR for sale in pokemon_sales) if num_sales > 0 else 0
    min_price = min(sale.card_price_EUR for sale in pokemon_sales) if num_sales > 0 else 0

    kpis = {'num_sales': num_sales, 'avg_price': avg_price, 'max_price': max_price, 'min_price': min_price}

    return render_template('results.html', pokemon_name=pokemon_name, pokemon_sales=pokemon_sales, kpis=kpis, selectedImageLink = request.args.get('selectedImageLink', ''))




if __name__ == '__main__':
    app.run(debug=True)