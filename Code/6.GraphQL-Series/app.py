from flask import Flask, request, jsonify
from ariadne import graphql_sync, load_schema_from_path, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL
from schema.resolvers import query, mutation, user_object

type_defs = load_schema_from_path("schema/type_defs.graphql")
schema = make_executable_schema(type_defs, query, mutation, user_object)

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return ExplorerGraphiQL().html(None), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
