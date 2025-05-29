import json
from collections import defaultdict

def rdf_to_markdown(json_file, markdown_file):
    """
    Converts RDF data in a JSON file into a Markdown file.

    Args:
        json_file (str): Path to the JSON file containing RDF data.
        markdown_file (str): Path to the output Markdown file.
    """
    with open(json_file, "r") as file:
        data = json.load(file)

    # Open the Markdown file for writing
    with open(markdown_file, "w") as md_file:
        for binding in data["results"]["bindings"]:
            # Extract the property and value
            property_uri = binding["property"]["value"]
            value = binding["hasValue"]["value"]

            # Write the property as a header
            md_file.write(f"## {property_uri}\n\n")

            # Write the value as text under the header
            md_file.write(f"{value}\n\n")

def rdf_to_markdown_grouped(json_file, markdown_file):
    """
    Converts RDF data in a JSON file into a Markdown file, grouping multiple values of a property under one heading.

    Args:
        json_file (str): Path to the JSON file containing RDF data.
        markdown_file (str): Path to the output Markdown file.
    """
    with open(json_file, "r") as file:
        data = json.load(file)

    # Group values by property
    grouped_data = defaultdict(list)
    for binding in data["results"]["bindings"]:
        property_uri = binding["property"]["value"]
        value = binding["hasValue"]["value"]
        grouped_data[property_uri].append(value)

    # Write grouped data to the Markdown file
    with open(markdown_file, "w") as md_file:
        for property_uri, values in grouped_data.items():
            # Write the property as a header
            md_file.write(f"## {property_uri}\n\n")
            # Write all values under the header
            for value in values:
                md_file.write(f"- {value}\n")
            md_file.write("\n")

if __name__ == "__main__":
    # Input JSON file and output Markdown file
    json_file = "/Users/johnthomas/Documents/existing.json"
    markdown_file = "/Users/johnthomas/Documents/output.md"

    # Convert RDF data to Markdown
    rdf_to_markdown_grouped(json_file, markdown_file)
    print(f"Markdown file created at: {markdown_file}")
