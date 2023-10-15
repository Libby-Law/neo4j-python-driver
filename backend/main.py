from flask import Flask, render_template, request
import neo4j

app = Flask(__name__)

NEO4J_URI = "neo4j+s://a189df45.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "akLGQO8dxzvbQq--n-BoD9L2X-QCsxiKS1-__ybeocQ"
driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

@app.route('/', methods=['GET', 'POST'])
def index():
    result_df = None
    if request.method == 'POST':
        query = request.form['query']
        with driver.session() as session:
            result = session.run(query)
            result_df = result.to_df()

    return render_template('index.html', result_df=result_df)

if __name__ == '__main__':
    app.run(debug=True)
