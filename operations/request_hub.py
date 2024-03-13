from identify_viability import main as identify_viability_main

from flask import Flask
api = Flask(__name__)

@api.route('/identify_viability', methods=['PUT'])
def call_identify_viability():
    response = identify_viability_main()
    return response

if __name__ == '__main__':
    api.run()