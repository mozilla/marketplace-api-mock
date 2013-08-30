import app


@app.route('/api/v1/services/region/')
def regions_list():
    def gen():
        i = 1
        while 1:
            yield app.defaults.region(id=i, slug='region-%d' % i)
            i += 1

    data = app._paginated('objects', gen, 25)
    return data


@app.route('/api/v1/services/region/<slug>')
def regions_get(slug):
    return app.defaults.region()


@app.route('/api/v1/services/carrier/')
def carriers_list():
    def gen():
        i = 1
        while 1:
            yield app.defaults.carrier(id=i, slug='carrier-%d' % i)
            i += 1

    data = app._paginated('objects', gen, 25)
    return data


@app.route('/api/v1/services/carrier/<slug>')
def carriers_get(slug):
    return app.defaults.carrier()
