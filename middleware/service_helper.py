import requests
import json

def get_order_ids(orderID):
    try:
        # local testing
        # url_call = "http://192.168.0.119:5002/orders/" + str(orderID)
        url_call = "http://44.197.87.209:5000/orders/" + str(orderID)
        response = requests.get(url_call)
        if response.status_code==200:
            details = json.loads(response.text)

            return {
                "userID": details.get('data')[0].get('customer'),
                "productID": details.get('data')[0].get('part'),
                "orderID": orderID
            }
        else:
            raise Exception("Could not GET order details!")

    except:
        raise Exception("GET request failed!")




def generate_urls(data):
    # replace with endpoint urls
    url_dict = {
        # Local testing
        # "UserAddress": "http://127.0.0.1:5000/",
        # "Product": "http://192.168.0.119:5001/",
        # "Orders": "http://192.168.0.119:5002/",
        "UserAddress": "http://Eb2-env.eba-khxuypq3.us-east-1.elasticbeanstalk.com/",
        "Product": "http://3.81.181.29:5000/",
        "Orders": "http://44.197.87.209:5000/",
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
