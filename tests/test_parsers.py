import unittest
from parsers import logcat_summary,permissions_summary

class ParserTests(unittest.TestCase):
    def test_logcat_no_messages(self):
        r=logcat_summary('09-14 10:20:30.000 100 101 E Example: password=never-store-this\n09-14 10:20:31.000 100 101 E Example: token=also-secret')
        self.assertEqual(r['total_errors'],2);self.assertEqual(r['groups'][0]['count'],2);self.assertNotIn('never-store',str(r));self.assertNotIn('also-secret',str(r))
    def test_permission_states(self):
        r=permissions_summary('android.permission.CAMERA: granted=false\nandroid.permission.INTERNET: granted=true')
        self.assertFalse(r['permissions']['android.permission.CAMERA']);self.assertTrue(r['permissions']['android.permission.INTERNET'])
    def test_empty_not_complete(self):self.assertFalse(permissions_summary('')['complete'])
