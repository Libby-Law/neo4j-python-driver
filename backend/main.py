from flask import Flask, render_template, request, jsonify
import neo4j
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Restrict CORS to the React app's domain

NEO4J_URI = "neo4j+s://a189df45.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "akLGQO8dxzvbQq--n-BoD9L2X-QCsxiKS1-__ybeocQ"
driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def transform_neo4j_result_to_force_graph_format(records):
    nodes = []
    links = []
    
    added_nodes = set()

    for record in records:
        source_node = record['n']
        target_node = record['m']

        if source_node.id not in added_nodes:
            nodes.append({"id": source_node.id, "label": dict(source_node)['name'] if 'name' in dict(source_node) else str(source_node.id)})
            added_nodes.add(source_node.id)

        if target_node.id not in added_nodes:
            nodes.append({"id": target_node.id, "label": dict(target_node)['name'] if 'name' in dict(target_node) else str(target_node.id)})
            added_nodes.add(target_node.id)

        links.append({
            "source": source_node.id,
            "target": target_node.id,
        })

    return {"nodes": nodes, "links": links}

@app.route('/', methods=['GET', 'POST'])
def index():
    result_df = None
    if request.method == 'POST':
        query = request.form['query']
        with driver.session() as session:
            result = session.run(query)
            result_df = result.to_df()

    return render_template('index.html', result_df=result_df)

@app.route('/get_graph_data')
def get_graph_data():
    with driver.session() as session:
        result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m;")
        data = transform_neo4j_result_to_force_graph_format(result)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
