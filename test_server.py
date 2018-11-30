from server import *
import unittest


class TestServer(unittest.TestCase):
    def test_load_config(self):
        self.assertEqual(load_config())

    def test_main_wo_args(self):
        self.assertEqual(main())

    def test_main_with_args(self):
        self.assertEqual(main(sys.argv[1:]))

    def test_usage(self):
        self.assertEqual(usage())

    def test_server_wo_args(self):
        self.assertEqual(server())

    def test_server_with_args(self):
        self.assertEqual(server(sys.argv[1:]))


if __name__ == '__main__':
    unittest.main()
