from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'dpbedia interfacing test go!'

class dbPediaConnector:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self.sparql.setReturnFormat(JSON)
        self.sparql.setMethod('GET')

    def get_data(self, query):
        self.sparql.setQuery(query)
        results = self.sparql.queryAndConvert()
        return results


def find_pages_based_on_name(name):
    query = f"""
    SELECT ?entity ?comment ?label
        WHERE {{
            ?entity rdfs:label ?label ;
                    rdfs:comment ?comment .
            ?label bif:contains "{name}" OPTION (score ?sc , score_limit 15) 
        FILTER langMatches(lang(?label),'en')
        FILTER langmatches(lang(?comment), 'en')
    }}
    """
    connector = dbPediaConnector()
    results = connector.get_data(query)
    return results

def get_resource_from_uri(uri):
    query = f"""
    SELECT ?property ?hasValue ?isValueOf
        WHERE {{ <{uri}> ?property ?hasValue
        FILTER (
            (isIRI(?hasValue) ||  # Keep URIs (no language tag)
            (lang(?hasValue) = "en") ||  # Keep English literals
            (!langMatches(lang(?hasValue), "*")))  # Keep literals without language tag
            &&
            ?property NOT IN (rdf:type, foaf:depiction, owl:sameAs))
}}
    """
    connector = dbPediaConnector()
    results = connector.get_data(query)
    return results

def rdf_to_markdown_grouped(data):
    """
    Converts RDF data in a JSON into a Markdown string, grouping multiple values of a property under one heading.
    """

    # Group values by property
    grouped_data = defaultdict(list)
    for binding in data["results"]["bindings"]:
        property_uri = binding["property"]["value"]
        value = binding["hasValue"]["value"]
        grouped_data[property_uri].append(value)

    # Write grouped data to a markdown string 
    output_list = []
    for property_uri, values in grouped_data.items():
        # Write the property as a header
        output_list.append("## {property_uri}\n\n")
        # Write all values under the header
        for value in values:
            output_list.append(f"- {value}\n")
        output_list.append("\n")
    return ''.join(output_list)

@app.route('/page/<name>', methods=['GET'])
def get_page_by_name(name):
    results = find_pages_based_on_name(name)
    if not results:
        return jsonify({'error': 'No results found'}), 404
    return jsonify(results)

@app.route('/resource', methods=['GET'])
def get_resource_and_return_markdown():
    uri = request.args.get('uri')
    results = get_resource_from_uri(uri)
    if not results:
        return jsonify({'error': 'No results found'}), 404
    return rdf_to_markdown_grouped(results)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
    


