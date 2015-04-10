__author__ = 'nathan'

import unittest
import pytest

try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock, MagicMock


class MyTestCase(unittest.TestCase):
    def test_(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
