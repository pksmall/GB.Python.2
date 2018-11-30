from client import *
import unittest


class TestClient(unittest.TestCase):
    def test_load_config(self):
        self.assertEqual(load_config())

    def test_main_wo_args(self):
        self.assertEqual(main())

    def test_main_with_args(self):
        self.assertEqual(main(sys.argv[1:]))

    def test_usage(self):
        self.assertEqual(usage())

    def test_date_wo_args(self):
        self.assertEqual(date())

    def test_date_with_args(self):
        self.assertEqual(date(time.time(), '%Y-%m-%d %H:%M:%S'))

    def test_client_wo_args(self):
        self.assertEqual(client())

    def test_client_with_args(self):
        self.assertEqual(client(sys.argv[1:]))


if __name__ == '__main__':
    unittest.main()
