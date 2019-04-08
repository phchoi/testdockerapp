import falcon
import requests
import json

class Resource(object):
    def __init__(self):
        self.valid_params = ['title']
        self.valid_params_set = set(self.valid_params)
        self.all_params = {}
        self.all_params_set = set(self.all_params)
        self.params_limit = 10
        self.om_api_key = self.read_om_api_key('/app/config.ini')['om_api_key']
        self.api_endpoint = 'http://www.omdbapi.com/?apikey={}'.format(self.om_api_key)
        self.api_lookup_map = {
                               'title': 't',                            
                               'id'   : 'i'
                              }

    def on_get(self, req, resp):
        
        self.validate_params(req)

        print("{} {}".format(req.remote_addr, req))
        if req.params['title']:
            message = self.lookup_omdb('title', req.params['title'])
            out = { 'message': message }

        if out:
            resp.body = json.dumps(out)
            resp.status = falcon.HTTP_200
        else:
            raise falcon.HTTPBadRequest('Error', 'Something is not alright, please contact administrator')

    def lookup_omdb(self, lookup_type, lookup_value):
        search_string = { self.api_lookup_map[lookup_type]: lookup_value}
        response = requests.get(self.api_endpoint, params=search_string)
        data =  json.loads(response.text)
        print(data)

        result = {}
        message = ''
        if data['Response'] == 'True':
            result['title'] = data['Title']
            result['imdbid'] = data['imdbID']
            result['value'] = None
            for row in (data['Ratings']):
                if row['Source'] == 'Rotten Tomatoes':
                    result['value'] = row['Value']

        if len(result) > 0 and result['value'] is not None:
            message = ('You searched for {} "{}" and we found "{}"(imdbID: {}) ' + 
                       'with ratings {}, enjoy').format(lookup_type,
                                                                lookup_value,
                                                                result['title'],
                                                                result['imdbid'],
                                                                result['value'])
        elif len(result) > 0 and result['value'] is None:
            message = ('You searched for {} "{}" and we found "{}"(imdbID: {}) ' +
                       'with no Rotten Tomatoes ratings').format(lookup_type,
                                                                 lookup_value,
                                                                 result['title'],
                                                                 result['imdbid'])
        elif len(result) == 0:
            message = ('You searched for {} "{}" and ' + 
                       'we found nothing match').format(lookup_type,
                                                      lookup_value)

        #print(result)
        #print(message)

        return message

    def validate_params(self, req):
        if 'title' not in req.params:
             raise falcon.HTTPMissingParam('title')

        if self.all_params_set - self.valid_params_set:
            invalid_params = ', '.join(self.all_params_set - self.valid_params_set)
            raise falcon.HTTPInvalidParam('Only one of the below params are accepted {}'.format(self.valid_params), invalid_params) 

        if len(req.params.keys()) >= self.params_limit:
             raise falcon.HTTPBadRequest('Too many parameters','Too many parameters')


    def read_om_api_key(self, path):
        lines = {}
        with open(path, 'r') as file:
            for line in file:
                key, value = line.rstrip('\n').split('=')
                lines[key] = value
            #data = file.read().replace('\n', '')
        return lines
