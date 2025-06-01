from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Hello, Flask!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
