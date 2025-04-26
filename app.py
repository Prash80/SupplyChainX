from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime
from ai_engine import predict_delay
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Status color mapping function
def get_status_color(status):
    status_colors = {
        'On Time': 'success',
        'Delayed': 'warning',
        'In Transit': 'info',
        'Pending': 'secondary',
        'Completed': 'primary',
        'Cancelled': 'danger'
    }
    return status_colors.get(status, 'secondary')

# Context processor to make get_status_color available to all templates
@app.context_processor
def utility_processor():
    return dict(get_status_color=get_status_color)

# Initialize blockchain
blockchain = Blockchain()

# Load user data
def load_users():
    try:
        with open('data/users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Load shipment data
def load_shipments():
    try:
        with open('data/shipments.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save shipment data
def save_shipments(shipments):
    with open('data/shipments.json', 'w') as f:
        json.dump(shipments, f, indent=4)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    shipments = load_shipments()
    return render_template('dashboard.html', 
                         shipments=shipments,
                         username=session['username'],
                         role=session['role'])

@app.route('/shipment/<shipment_id>')
def shipment_detail(shipment_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    shipments = load_shipments()
    shipment = next((s for s in shipments if s['id'] == shipment_id), None)
    
    if not shipment:
        return redirect(url_for('dashboard'))
    
    return render_template('shipment_detail.html',
                         shipment=shipment,
                         username=session['username'],
                         role=session['role'])

@app.route('/ledger')
def ledger():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session['role'] not in ['admin', 'manager']:
        return redirect(url_for('dashboard'))
    
    return render_template('ledger.html',
                         chain=blockchain.chain,
                         username=session['username'],
                         role=session['role'])

@app.route('/about')
def about():
    return render_template('about.html',
                         username=session.get('username'),
                         role=session.get('role'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/shipments', methods=['GET'])
def get_shipments():
    shipments = load_shipments()
    return jsonify(shipments)

@app.route('/api/shipments', methods=['POST'])
def create_shipment():
    if 'username' not in session or session['role'] not in ['admin', 'manager']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    shipments = load_shipments()
    
    new_shipment = {
        'id': str(len(shipments) + 1),
        'origin': data['origin'],
        'destination': data['destination'],
        'eta': data['eta'],
        'status': 'Pending',
        'progress': 0,
        'created_at': datetime.now().isoformat(),
        'last_update': datetime.now().isoformat()
    }
    
    shipments.append(new_shipment)
    save_shipments(shipments)
    
    # Log the creation in blockchain
    blockchain.log_shipment_update(
        shipment_id=new_shipment['id'],
        update_type='creation',
        details={
            'created_by': session['username'],
            'origin': new_shipment['origin'],
            'destination': new_shipment['destination']
        }
    )
    
    return jsonify(new_shipment)

@app.route('/api/shipments/<shipment_id>/update', methods=['POST'])
def update_shipment(shipment_id):
    if 'username' not in session or session['role'] not in ['admin', 'manager']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    shipments = load_shipments()
    shipment = next((s for s in shipments if s['id'] == shipment_id), None)
    
    if not shipment:
        return jsonify({'error': 'Shipment not found'}), 404
    
    new_status = request.form.get('status')
    notes = request.form.get('notes')
    
    if new_status:
        shipment['status'] = new_status
        shipment['last_update'] = datetime.now().isoformat()
        
        # Log the update in blockchain
        blockchain.log_shipment_update(
            shipment_id=shipment_id,
            update_type='status_change',
            details={
                'new_status': new_status,
                'notes': notes,
                'updated_by': session['username']
            }
        )
        
        save_shipments(shipments)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid update'}), 400

@app.route('/api/predict-delay/<shipment_id>', methods=['GET'])
def get_delay_prediction(shipment_id):
    shipments = load_shipments()
    shipment = next((s for s in shipments if s['id'] == shipment_id), None)
    if shipment:
        prediction = predict_delay(shipment)
        return jsonify({'prediction': prediction})
    return jsonify({'error': 'Shipment not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 