import requests

COURIER_URL = "https://api.courier.com/send"


class CourierEmailWrapper:
    @classmethod
    def process_courier_request_data(cls, data):
        ''' Process the request body data for courier service

        :param data: request.data
        :return:
        '''

        try:
            emails = data.get('emails', None)
            phone_numbers = data.get('phone_numbers', None)
            title = data.get('title', None)
            body = data.get('body', None)
            channels = data.get('channels', None)
            elements = data.get('elements', None)
            dataset = data.get('data', None)

            missing_fields = []

            if emails is None:
                missing_fields.append("emails")
            if title is None:
                missing_fields.append("title")
            if body is None:
                missing_fields.append("body")
            if channels is None:
                missing_fields.append("channels")

            if len(missing_fields) > 0:
                raise Exception("The following required fields are missing: {}".format(",".join(missing_fields)))
            else:
                payload = cls.build_message(recipient_emails=emails, title=title, body=body,
                                            channels=channels,
                                            elements=elements, data=dataset)
            return payload
        except Exception as e:
            raise e

    @classmethod
    def build_message(cls, recipient_emails: list[str], title: str, body: str, channels: list[str],
                      recipient_phone_numbers: list[str] = None,
                      version: str = None, data: object = None, elements: list[object] = None,
                      providers: object = None):
        ''' Build a message object for courier service
        See https://www.courier.com/docs/reference/send/message/

        :param recipient_phone_numbers:
        :param recipient_emails:
        :param title:
        :param body:
        :param channels:
        :param version:
        :param data:
        :param elements:
        :param providers:
        :return:
        '''

        try:
            if elements is None:
                elements = []
            if data is None:
                data = {}
            if version is None:
                version = "1.0.0"
            if providers is None:
                providers = {}
            if recipient_phone_numbers is None:
                recipient_phone_numbers = []

            to_object = [{"email": r} for r in recipient_emails]

            if len(recipient_phone_numbers) > 0:
                to_object = [{"phone_number": r} for r in recipient_phone_numbers]

            return {
                "message": {
                    "to": to_object,
                    "content": {
                        "title": title,
                        "body": body,
                        "version": version,
                        "elements": elements
                    },
                    "data": data,
                    "routing": {
                        "method": "all",
                        "channels": channels
                    },
                    "providers": providers
                }
            }
        except Exception as e:
            raise e

    @classmethod
    def send_request(cls, auth_token, payload):
        try:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(auth_token)
            }

            return requests.post(COURIER_URL, json=payload, headers=headers)
        except Exception as e:
            raise e
