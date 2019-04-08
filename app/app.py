import falcon
import movie

api = falcon.API()
#api = application = falcon.API()


movie = movie.Resource()
api.add_route('/movie', movie)
