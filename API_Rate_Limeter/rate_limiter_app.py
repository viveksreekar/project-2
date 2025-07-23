import time
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# --- In-Memory Store for Token Buckets ---
# In a production environment, you would use a more persistent and scalable
# data store like Redis or Memcached to store the token buckets.
# For this example, a simple Python dictionary is sufficient to demonstrate
# the concept. The key will be the user identifier (e.g., IP address)
# and the value will be their token bucket object.
user_buckets = {}

class TokenBucket:
    """
    A class to implement the Token Bucket algorithm for rate limiting.
    """
    def __init__(self, capacity, refill_rate):
        """
        Initializes a new TokenBucket.

        Args:
            capacity (int): The maximum number of tokens the bucket can hold.
            refill_rate (float): The number of tokens to add per second.
        """
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity) # Start with a full bucket
        self.last_refill_time = time.time()

    def _refill(self):
        """
        Calculates and adds new tokens to the bucket based on the time elapsed
        since the last refill.
        """
        now = time.time()
        time_delta = now - self.last_refill_time
        # Calculate how many new tokens to add
        tokens_to_add = time_delta * self.refill_rate
        # Add the new tokens, but don't exceed the bucket's capacity
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now

    def consume(self, num_tokens=1):
        """
        Attempts to consume a specified number of tokens from the bucket.

        Args:
            num_tokens (int): The number of tokens to consume.

        Returns:
            bool: True if the tokens were consumed successfully, False otherwise.
        """
        self._refill() # Always refill before consuming
        if self.tokens >= num_tokens:
            self.tokens -= num_tokens
            return True
        return False

# --- Flask Application Setup ---
app = Flask(__name__)
# Allow requests from any origin for the frontend to work
CORS(app)


# --- Rate Limiter Decorator ---
def rate_limit(capacity, refill_rate):
    """
    A decorator that applies rate limiting to a Flask route.

    Args:
        capacity (int): The token bucket capacity for each user.
        refill_rate (float): The token refill rate per second.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Identify the user by their IP address. In a real app, you might
            # use an API key, user ID from a session, or a JWT.
            user_id = request.remote_addr

            # Get or create the user's token bucket
            if user_id not in user_buckets:
                user_buckets[user_id] = TokenBucket(capacity, refill_rate)

            bucket = user_buckets[user_id]

            # Try to consume a token
            if bucket.consume():
                # Success! Proceed with the request.
                return f(*args, **kwargs)
            else:
                # Not enough tokens. Deny the request.
                response = jsonify({
                    "error": "Too Many Requests",
                    "message": "You have exceeded the API rate limit."
                })
                response.status_code = 429 # HTTP status for Too Many Requests
                return response
        return decorated_function
    return decorator

# --- API Routes ---

@app.route('/')
def serve_index():
    """Serves the index.html file."""
    return send_from_directory('.', 'index.html')

@app.route('/unprotected')
def unprotected_endpoint():
    """An endpoint that is not rate-limited."""
    return jsonify({"message": "This is an unprotected endpoint. Feel free to call it as much as you want!"})

@app.route('/protected')
@rate_limit(capacity=5, refill_rate=1) # Allow 5 requests, then refill 1 token per second
def protected_endpoint():
    """
    A rate-limited endpoint.
    This configuration allows for a burst of 5 requests, after which the user
    must wait for tokens to be refilled at a rate of 1 per second.
    """
    return jsonify({"message": "Success! You have accessed the protected endpoint."})

# --- Main Execution ---
if __name__ == '__main__':
    # Running on 0.0.0.0 makes the server accessible from your local network.
    # Use http://127.0.0.1:5000 or http://localhost:5000 in your browser/client.
    app.run(host='0.0.0.0', port=5000, debug=True)
