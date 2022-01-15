from core_api import create_app

APP = create_app()

@APP.route("/")
def hello_world():
    return APP.send_static_file('index.html')

if __name__ == "__main__":
    APP.run(debug=True)
