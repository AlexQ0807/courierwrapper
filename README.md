## Wrapper for Courier API (Private)
<hr>

### Setup
```
pip install git+https://github.com/AlexQ0807/courierwrapper.git
```


### Example

```
from courierwrapper.email import CourierEmailWrapper

# Find out at: https://app.courier.com/settings/api-keys
COURIER_AUTH_TOKEN=<your_courier_auth_token> 

RECEIVER_EMAIL=<email_address_to_send_to>

data = {
    "emails": [RECEIVER_EMAIL],
    "title": "Test Email",
    "body": '''
        Hello World
    ''',
    "channels": ["email"],
}

payload = CourierEmailWrapper.process_courier_request_data(data)
response = CourierEmailWrapper.send_request(auth_token=COURIER_AUTH_TOKEN, payload=payload)

```