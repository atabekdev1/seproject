from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('API_KEY')

# Print the key to the console to verify that it's loaded
print(f"API Key: {api_key}")

# You can use the API key in your code, for example:
if api_key:
    print("API Key successfully loaded!")
else:
    print("API Key is missing or not loaded.")
