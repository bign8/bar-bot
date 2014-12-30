

class Order(object):
    drinks = set()
    guid = None
    user = None
    stamp = None

    @property
    def total(self):
        costs = [drink.cost for drink in self.drinks]
        return sum(costs)
