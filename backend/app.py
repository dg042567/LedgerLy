from flask import Flask, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# Replace with your Supabase keys

supabase_url = os.getenv("SUPABASE_URL")   
supabase_key = os.getenv("SUPABASE_KEY")   


supabase: Client = create_client(supabase_url, supabase_key)


@app.route('/add', methods=['POST'])
def add_transaction():
    data = request.json
    res = supabase.table('transactions').insert(data).execute()
    return jsonify(res.data), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    res = supabase.table('transactions').select("*").order("date", desc=True).execute()
    return jsonify(res.data)

if __name__ == '__main__':
    app.run(debug=True)
