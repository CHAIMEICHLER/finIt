"""Fake database API

Please don't learn anything from this file. It was done quick-and-dirty since it is not the point
of this demo. The point is the REST API."""


class Item:
    num = 0

    def __init__(self, name, code, price):
        self.name = str(name)
        self.code = int(code)
        self.price = float(price)
        Item.num += 1
        self.num = Item.num

    def __eq__(self, other):
        if isinstance(other, Item):
            other = other.num
        return self.num == other

    def update(self, vals):
        if 'name' in vals:
            self.name = str(vals['name'])
        if 'code' in vals:
            self.code = int(vals['code'])
        if 'price' in vals:
            self.price = float(vals['price'])

    def to_dict(self):
        return {'num': self.num, 'name': self.name, 'code': self.code, 'price': self.price}


class Sale:
    num = 0

    def __init__(self, item_num, amount, price):
        self.item_num = int(item_num)
        self.amount = int(amount)
        self.price = float(price)
        Sale.num += 1
        self.num = Sale.num

    def __eq__(self, other):
        if isinstance(other, Sale):
            other = other.num
        return self.num == other

    def to_dict(self):
        return {'num': self.num, 'item_num': self.item_num, 'amount': self.amount, 'price': self.price}

items = []
sales = []


def get_all_items():
    lst = []
    for item in items:
        d = item.to_dict()
        del d['price']
        lst.append(d)
    return lst


def _get_item(num):
    for item in items:
        if item == num:
            return item
    raise ValueError


def get_item(num):
    return _get_item(num).to_dict()


def add_item(name, code, price):
    item = Item(name, code, price)
    items.append(item)
    return item.to_dict()


def remove_item(num):
    item = _get_item(num)
    items.remove(item)
    lst = get_item_sales(num)
    for sale in lst:
        remove_sale(sale.num)
    return item.to_dict().update(num_sales=len(lst))


def change_item(num, new_vals):
    item = _get_item(num)
    item.update(new_vals)
    return item.to_dict()


def duplicate_item(num):
    item = _get_item(num)
    return add_item(item.name, item.code, item.price)


def get_all_sales():
    lst = []
    for sale in sales:
        d = sale.to_dict()
        item = _get_item(sale.item_num)
        d['item_name'] = item.name
        lst.append(d)
    return lst


def _get_sale(num):
    for sale in sales:
        if sale == num:
            return sale
    raise ValueError


def get_sale(num):
    sale = _get_sale(num)
    d = sale.to_dict()
    item = _get_item(sale.item_num)
    d['item'] = item.to_dict()
    return d


def add_sale(item_num, amount, price):
    sale = Sale(item_num, amount, price)
    sales.append(sale)
    return sale.to_dict()


def remove_sale(num):
    sale = _get_sale(num)
    sales.remove(sale)
    return sale.to_dict()


def get_item_sales(item_num):
    item_sales = []
    for sale in sales:
        if sale.item_num == item_num:
            item_sales.append(sale.to_dict())
    return item_sales