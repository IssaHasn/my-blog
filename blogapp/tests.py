from django.test import TestCase, Client
from django.urls import reverse

# -----models tests
from .models import User, Post

# User Test
class UserTest(TestCase):

    #test create user
    def test_create_user(self):

        user = User.objects.create(name="Ali hasn")

        self.assertEqual(user.name, "Ali hasn")

    #test user name validation (user name > max length(255) or user name is empty)
    def test_user_name(self):
    
        try:
            User.objects.create(name="This name is way too long to be valid "*10)

        except ValidationError as e:
            self.assertEqual(e.message_dict, {"name": ["Name is too long."]})

        except Exception as e:
            self.fail("Unexpected exception raised: {}".format(e))
        
        try:
            User.objects.create(name="")

        except ValidationError as e:
            self.assertEqual(e.message_dict, {"name": ["This field is required."]})
            
        except Exception as e:
            self.fail("Unexpected exception raised: {}".format(e))


# Post Test
class PostTest(TestCase):
    
    #test create post
    def test_create_post(self):

        author = User.objects.create(name="Ali hasn")
        post = Post.objects.create(
            title="My Post",
            slug="my-post",
            author=author,
            body="This is my post.",
        )

        self.assertEqual(post.title, "My Post")
        self.assertEqual(post.slug, "my-post")
        self.assertEqual(post.author, author)
        self.assertEqual(post.body, "This is my post.")
        self.assertEqual(post.status, Post.Status.DRAFT)

# Comment Test

#-----views tests
class BlogViewsTest(TestCase):

    #simple setup
    def setUp(self):

        self.client = Client()
    
    #Tests successful rendering of the home page.
    def test_home_page_view(self):
        
        response = self.client.get(reverse('blog:home_page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    #Tests successful rendering of the posts page.
    def test_posts_page_view(self):
        
        response = self.client.get(reverse('blog:posts_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')

    #Tests successful rendering of the post detail page for an existing post.
    def test_post_detail_view_existing_post(self):

        post = Post.objects.create(title='Test Post', body='This is a test post.')
        response = self.client.get(reverse('blog:post_detail', args=[post.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/detail.html')
        self.assertContains(response, post.title)
        self.assertContains(response, post.body)

    #Tests that a 404 error is raised for a nonexistent post.
    # def test_post_detail_view_nonexistent_post(self):

    #     nonexistent_id = 1000  # This post not found
    #     response = self.client.get(reverse('blog:post_detail', args=[nonexistent_id]))

    #     self.assertTemplateUsed(response, 'blog/post/post404.html')
        