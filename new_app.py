# Add this near your other route definitions
users = {
    "admin": "password123",  # In production, use hashed passwords!
    "user": "smarthat2023"
}

from functools import wraps
import jwt
import datetime

# Secret key for JWT - change this in production!
JWT_SECRET = "your_very_secret_key_here"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    auth = request.json
    
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Could not verify'}), 401
    
    if auth['username'] in users and auth['password'] == users[auth['username']]:
        token = jwt.encode({
            'username': auth['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, JWT_SECRET)
        
        return jsonify({'token': token})
        
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/verify', methods=['GET'])
def verify():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
    
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
        
    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return jsonify({'message': 'Token is valid'})
    except:
        return jsonify({'message': 'Token is invalid!'}), 401

# Protect your existing routes by adding @token_required decorator
@app.route('/status')
@token_required
def protected_status(current_user):
    # Your existing status code
    battery = psutil.sensors_battery()
    return jsonify({
        "battery": battery.percent if battery else -1,
        "health": health_status,
        "detection_active": detection_active,
        "quiet_mode_enabled": config_data.get("quiet_mode_enabled", False),
        "mode": "indoor" if config_data.get("indoor_mode") else "outdoor"
    })
