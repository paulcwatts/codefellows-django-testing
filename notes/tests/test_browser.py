import os
from selenium import webdriver

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

#
# Note: You can just do something like this:
# from selenium import webdriver
#
# def setUpClass(cls):
#    cls.selenium = webdriver.Firefox()
#
# However, this method allows you to change which browser is tested.
# This is useful if you are running tests from a CI server and want to
# test as many browsers as you can.
#
WEBDRIVER_CLASS_NAME = os.environ.get('WEBTEST_DRIVER', 'Chrome')


class BrowserTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = getattr(webdriver, WEBDRIVER_CLASS_NAME)()
        super(BrowserTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BrowserTest, cls).tearDownClass()

    def test_autofocus_add(self):
        "Tests that the textarea in the add form is autofocused."
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('note-add')))
        textarea = self.selenium.find_element_by_name("note")
        active = self.selenium.switch_to_active_element()
        self.assertEqual(textarea, active,
                         "textarea should be focused, but {0} is instead".format(
                             active.tag_name
                         ))
