from django.test import TestCase


class ImageDetectorTest(TestCase):
    """Test cases for image detector."""
    
    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detector/index.html')
