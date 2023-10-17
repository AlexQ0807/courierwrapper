import os
import traceback
from datetime import datetime

from courierwrapper.email import CourierEmailWrapper

import unittest

from dotenv import load_dotenv
load_dotenv()

COURIER_AUTH_TOKEN = os.getenv("COURIER_AUTH_TOKEN")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


class TestSQLAlchemyEngineWrapper(unittest.TestCase):

    def test_simple_courier_send(self):
        try:
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

            self.assertTrue(200 <= response.status_code <= 299)
        except Exception as e:
            traceback.print_exc()
            self.assertTrue(False)

    def test_markup_courier_send(self):
        '''
        Resource:
        https://www.courier.com/blog/introducing-courier-elemental/

        :return:
        '''
        try:
            data = {
                "emails": [RECEIVER_EMAIL],
                "title": "Test Email with Markup (Courier Elemental)",
                "body": "Email Test {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                "channels": ["email"],
                "elements": [
                    {
                        "type": "group",
                        "loop": "data.posts",
                        "elements": [
                            {
                                "type": "text",
                                "content": "Name: **{{$.item.name}}**  "
                            },
                            {
                                "type": "text",
                                "content": "Composer: {{$.item.composer}}  "
                            },
                            {

                                "type": "image",
                                "src": "{{$.item.thumbnail}}",
                                "align": "center",
                                "altText": "{{$.item.composer}} Image"

                            },
                            {"type": "divider"}
                        ]
                    },
                ],
                "data": {
                    "posts": [
                        {
                            "name": "Piano Sonata No. 14",
                            "composer": "Ludwig van Beethoven",
                            "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Joseph_Karl_Stieler%27s_Beethoven_mit_dem_Manuskript_der_Missa_solemnis.jpg/330px-Joseph_Karl_Stieler%27s_Beethoven_mit_dem_Manuskript_der_Missa_solemnis.jpg",
                        },
                        {
                            "name": "Piano Sonata No. 2",
                            "composer": "Frederic Chopin",
                            "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Frederic_Chopin_photo.jpeg/330px-Frederic_Chopin_photo.jpeg",

                        },
                        {
                            "name": "Gymnopedie No. 1",
                            "composer": "Erik Satie",
                            "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Ericsatie.jpg/330px-Ericsatie.jpg",
                        },
                        {
                            "name": "Clair de lune",
                            "composer": "Claude Debussy",
                            "thumbnail": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Claude_Debussy_atelier_Nadar.jpg/330px-Claude_Debussy_atelier_Nadar.jpg",
                        },
                    ]
                }
            }

            payload = CourierEmailWrapper.process_courier_request_data(data)
            response = CourierEmailWrapper.send_request(auth_token=COURIER_AUTH_TOKEN, payload=payload)

            self.assertTrue(200 <= response.status_code <= 299)
        except Exception as e:
            traceback.print_exc()
            self.assertTrue(False)