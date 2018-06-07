from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    
    
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Rdith goes to the home page and accidentally tries to submit
        #an empty list item. she hits enter an the empty imput box
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        #The home page refreshes, and there is na error message saying
        #that list items cannot be blank
        error = self.get_error_element()
        self.assertEqual(error.text, "you can't have an empty list item")
        
        #she tries again with some text for the item, which now works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')
        #perversely, she now decides to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        #She receives a similar warninig on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        
        #and she can correct it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
        self.fail('write me')


    def test_cannot_add_duplicate_item(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, 'You have got already this in your list')

    def test_error_messages_are_cleared_on_input(self):
        # Edith start a new list in a way that causes a validation error
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(' \n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # she start a typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')
        # she pleased to see that a error message disappear
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
