from django.test import TestCase


# Create your tests here.
from .models import Image, Profile, Follow, Comment


class TestImage(TestCase):
    def setUp(self):
        self. profile = Profile(name='home')
        self.profile.save_profile()

        self.follow = Follow(name='page')
        self.follow.save_follow()

        self.image_test = Image(id=1, name='image', description='this is a test image', profile=self.Profile,
                                profile=self.)

    def test_instance(self):
        self.assertTrue(isinstance(self.image_test, Image))

    def test_save_image(self):
        self.image_test.save_image()
        after = Image.objects.all()
        self.assertTrue(len(after) > 0)

    def test_delete_image(self):
        self.image_test.delete_image()
        images = Image.objects.all()
        self.assertTrue(len(images) == 0)

    def test_update_image(self):
        self.image_test.save_image()
        self.image_test.update_image(self.image_test.id, 'photos/test.jpg')
        changed_img = Image.objects.filter(image='photos/test.jpg')
        self.assertTrue(len(changed_img) > 0)

    def test_get_image_by_id(self):
        found_image = self.image_test.get_image_by_id(self.image_test.id)
        image = Image.objects.filter(id=self.image_test.id)
        self.assertTrue(found_image, image)

    def test_search_image_by_profile(self):
        self.image_test.save_image()
        found_images = self.image_test.filter_by_follow(profile='home')
        self.assertTrue(len(found_images) == 1)

    def test_search_image_by_follow(self):
        profile = 'page'
        found_img = self.image_test.search_by_profile(follow)
        self.assertTrue(len(found_img) > 1)

    def tearDown(self):
        Image.objects.all().delete()
        Profile.objects.all().delete()
        Follow.objects.all().delete()


