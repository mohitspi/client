from mainapp import create_app

app = create_app()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    # app.run(debug=True,port=5000)
    app.run(host="0.0.0.0", port=8080, debug = True)
