def generate_urls(data):
    # replace with endpoint urls
    url_dict = {
        "UserAddress": "http://192.168.0.119:5000/",
        "Product": "http://192.168.0.119:5001/",
        "Orders": "http://192.168.0.119:5002/",
    }

    if data.get('userID', False) and data.get('productID', False) and data.get('orderID'):
        url_list = []
        url_list.append(url_dict['UserAddress'] + 'users/' + str(data['userID']))
        url_list.append(url_dict['UserAddress'] + 'users/' + str(data['userID']) + '/address')
        url_list.append(url_dict['Product'] + 'products/' + str(data['productID']))
        url_list.append(url_dict['Orders'] + 'orders/' + str(data['orderID']))
        return url_list

    else:
        raise Exception("POST body missing essential fields!")

def strip_data(data):
    filter_list = [
        'pname', 'manufacturer', 'orderDateTime', 'quantity',
        'price', 'nameLast', 'nameFirst', 'username', 'email',
        'streetNo', 'streetName1', 'streetName2', 'city',
        'state', 'zipcode'
    ]

    resp_dict = dict()
    for details in data:
        for k, v in details['data'][0].items():
            if k in filter_list:
                resp_dict[k] = v

    return resp_dict
