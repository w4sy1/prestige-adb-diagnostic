import unittest
from app import choose_device,battery

class AdbTests(unittest.TestCase):
    def test_unauthorized(self):
        with self.assertRaises(ValueError):choose_device('List of devices attached\na unauthorized\n')
    def test_many_devices(self):
        with self.assertRaises(ValueError):choose_device('List of devices attached\na device\nb device\n')
    def test_selected(self):self.assertEqual(choose_device('List of devices attached\na device\nb device','b'),'b')
    def test_temperature(self):self.assertEqual(battery('temperature: 321')['temperature_c'],32.1)
    def test_empty_battery(self):self.assertIsNone(battery('')['temperature_c'])
