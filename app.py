from ext import app

if __name__ == "__main__":
    from routes import index, product, login, register, store, news, album

    app.run(debug=True)
