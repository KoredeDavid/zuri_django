from django.test import TestCase

from zuri.models import Post, CustomUser, Category


class MyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(email='test@email.com', username='KoredeDavid')
        category = Category.objects.create(name='Yahoo is the way', about='So ni CC')
        Post.objects.create(category=category, title="#InnosonMotors. A nice motor?", author=user,
                            body=' Proudly Nigerian')

    # This checks if the clean_slug function actually removes non alpha-numeric characters excluding whitespace
    def test_slug(self):
        post_slug = Post.objects.get(id=1).slug
        self.assertEqual('innosonmotors-a-nice-motor', str(post_slug), )

    # This ensures that the user's display name is exactly what the user inputs it
    # as the model usually turns them to lower-case for effective validation
    def test_display_name(self):
        display_name = CustomUser.objects.get(id=1).display_name
        self.assertEqual('KoredeDavid', str(display_name), )
