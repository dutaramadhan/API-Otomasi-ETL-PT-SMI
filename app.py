from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json


app = Flask(__name__)
load_dotenv()


if __name__ == '__main__':
    app.run(debug=True)