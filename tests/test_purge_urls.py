import unittest

from bin.purger import create_purge_command

class PurgeUrlsTestCase(unittest.TestCase):

    def setUp(self):
        self.cmd_template = 'random {path} template'

    def test_create_purge_command_valid_url(self):

        cmd = create_purge_command('http://domain/path/to/purge', self.cmd_template)
        expected = self.cmd_template.format(path='/path/to/purge')

        self.assertEqual(cmd, expected)

    def test_create_purge_command_invalid_url(self):

        cmd = create_purge_command('domain / path / t o / purge', self.cmd_template)
        self.assertIsNone(cmd)


if __name__ == '__main__':
    unittest.main()
