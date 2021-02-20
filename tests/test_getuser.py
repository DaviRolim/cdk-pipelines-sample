import unittest
from pipelines_webinar.lambda_rep import handler


class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("testing response.")
        result = handler.handler(None, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Access-Control-Allow-Origin'], '*')
        # self.assertIn('Hello World', result['body'])


if __name__ == '__main__':
    unittest.main()