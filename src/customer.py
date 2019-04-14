class Customer():

    def __init__(self, name, licence):
        self._name    = name
        self._licence = licence

    @property
    def name(self):
        return self._name

    @property
    def licence(self):
        return self._licence

    def __str__(self):
        return f'Customer <name: {self._name}, licence: {self._licence}>'

    def __eq__(self, other):
        return (self._name == other._name) and (self._licence == other._licence)

    def __ne__(self, other):
        return not (self == other)            
