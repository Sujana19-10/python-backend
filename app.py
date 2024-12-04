from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for CORS

# Access MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI', '')  # MongoDB URI from .env file

# Attempt to establish MongoDB connection
client = None
db = None
try:
    client = MongoClient(MONGO_URI)
    db = client.get_database()
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection failed: {str(e)}")

# Access backend URL from environment variables (this is for frontend configuration)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:5000')  # Default to local if not found

@app.route('/verify', methods=['POST'])
def verify_code():
    data = request.json
    user_code = data.get('code', '')
    level = data.get('level', 1)  # Default to Level 1 if not specified

    try:
        # Debugging: Print user code to verify it's being received correctly
        print("User code received:", user_code)

        # Level 1: Find maximum in an array
        if level == 1:
            array = [1, 3, 5, 7]
            expected_output = max(array)

            # Execute user code safely
            local_vars = {}
            try:
                exec(user_code, {}, local_vars)
            except Exception as e:
                return jsonify(correct=False, error=f"Error in user code execution: {str(e)}")

            user_function = local_vars.get('find_max', None)

            if callable(user_function):
                output = user_function(array)
                if output == expected_output:
                    return jsonify(correct=True)
                else:
                    return jsonify(correct=False, error="Incorrect output for Level 1.")
            else:
                return jsonify(correct=False, error="Function 'find_max' not defined.")

        # Level 2: Check if two strings are anagrams
        elif level == 2:
            input1 = "listen"
            input2 = "silent"
            expected_output = True  # They are anagrams

            # Execute user code safely
            local_vars = {}
            try:
                exec(user_code, {}, local_vars)
            except Exception as e:
                return jsonify(correct=False, error=f"Error in user code execution: {str(e)}")

            user_function = local_vars.get('are_anagrams', None)

            if callable(user_function):
                output = user_function(input1, input2)
                if output == expected_output:
                    return jsonify(correct=True)
                else:
                    return jsonify(correct=False, error="Incorrect output for Level 2.")
        
        # Level 3: Find the longest substring without repeating characters
        elif level == 3:
            s = "abcabcbb"
            expected_output = 3  # Longest substring without repeating characters is "abc"

            # Execute user code safely
            local_vars = {}
            try:
                exec(user_code, {}, local_vars)
            except Exception as e:
                return jsonify(correct=False, error=f"Error in user code execution: {str(e)}")

            # Debugging: Print the local variables to see if the function is defined
            print("Local variables after exec:", local_vars)

            # Check if the function is defined in the executed code
            user_function = local_vars.get('length_of_longest_substring', None)

            if callable(user_function):
                output = user_function(s)
                if output == expected_output:
                    return jsonify(correct=True)
                else:
                    return jsonify(correct=False, error="Incorrect output for Level 3.")
        
        else:
            return jsonify(correct=False, error="Invalid level specified.")

    except Exception as e:
        # Return detailed error information
        return jsonify(correct=False, error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Use 0.0.0.0 for production or cloud hosting
