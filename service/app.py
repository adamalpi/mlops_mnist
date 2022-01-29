import connexion
from connexion.resolver import RestyResolver
from flask_cors import CORS
from swagger_ui_bundle import swagger_ui_3_path

if __name__ == "__main__":
    options = {"swagger_path": swagger_ui_3_path}
    app = connexion.App(__name__, specification_dir="openapi/", options=options)
    app.add_api("app.yaml", resolver=RestyResolver("api"))

    CORS(app.app)

    app.run(port=9090, debug=True)

# http://localhost:9090/api/v1.0/ui/
# swagger editor https://editor.swagger.io/
