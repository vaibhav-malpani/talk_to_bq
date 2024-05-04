from flask import Flask, render_template, request
import google.generativeai as genai
import pandas_gbq as pd

app = Flask(__name__)
API_KEY = "<YOUR_API_KEY>"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest')


def generate_query(prompt):
    context = """
    you are suppose to write a SQL query. 
    You have a database of liquor sale.
    Database Name: bigquery-public-data.iowa_liquor_sales
    Table Name: sales
    While mentioning FROM <TABLE_NAME> always use <Database Name>.<Table Name>
    use the exact column names from the table content provided below.
    Do not add any column names on your own.. be very precise with you answer
    Table Content:
    [{
      "date": "2023-03-17",
      "store_name": "FAREWAY STORES #648 / OTTUMWA",
      "address": "1325 ALBIA RD",
      "city": "OTTUMWA",
      "zip_code": "52501.0",
      "item_description": "JAGERMEISTER LIQUEUR MINI MEISTERS",
      "pack": "12",
      "bottle_volume_ml": "20",
      "state_bottle_cost": "5.63",
      "state_bottle_retail": "8.45",
      "bottles_sold": "1",
      "sale_dollars": "8.45",
      "volume_sold_liters": "0.02"
    }, {
      "date": "2021-02-25",
      "store_name": "FAREWAY STORES #995 / PELLA",
      "address": "2010 WASHINGTON ST",
      "city": "PELLA",
      "zip_code": "50219.0",
      "item_description": "THE BITTER TRUTH COCKTAIL BAR PACK",
      "pack": "12",
      "bottle_volume_ml": "20",
      "state_bottle_cost": "9.5",
      "state_bottle_retail": "14.25",
      "bottles_sold": "2",
      "sale_dollars": "28.5",
      "volume_sold_liters": "0.04"
    }]
    get response as a raw sql query
    """

    prompt = context + prompt
    response = model.generate_content(prompt)
    query = response.text.replace("sql", "").replace("\n", " ").replace("```", "").replace("     ", " ")
    return query


def get_data_from_bq(prompt):
    query = generate_query(prompt)
    print(query)
    df = pd.read_gbq(query)
    return df.to_html()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_data', methods=['POST'])
def get_data():
    prompt = request.json['prompt']
    print(prompt)
    data = get_data_from_bq(prompt)
    return data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
