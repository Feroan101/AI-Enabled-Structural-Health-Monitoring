from flask import Flask, request, jsonify, render_template from flask_sqlalchemy import SQLAlchemy from datetime import datetime import random

app = Flask(name) app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shm_web.db' app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False db = SQLAlchemy(app)

class SensorData(db.Model): id = db.Column(db.Integer, primary_key=True) timestamp = db.Column(db.String(100)) vibration = db.Column(db.Float) stress = db.Column(db.Float) temperature = db.Column(db.Float)

@app.route('/') def index(): return render_template('index.html')

@app.route('/api/data', methods=['POST']) def receive_data(): data = request.json entry = SensorData( timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), vibration=data.get('vibration', 0.0), stress=data.get('stress', 0.0), temperature=data.get('temperature', 0.0) ) db.session.add(entry) db.session.commit() return jsonify({'status': 'success'})

@app.route('/api/data/latest', methods=['GET']) def get_latest(): latest = SensorData.query.order_by(SensorData.id.desc()).limit(20).all() results = [ { 'timestamp': row.timestamp, 'vibration': row.vibration, 'stress': row.stress, 'temperature': row.temperature } for row in latest[::-1] ] return jsonify(results)

if name == 'main': db.create_all() app.run(debug=True)

