from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField


# user reference 
User = get_user_model()

# post author 
class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(upload_to='users/%Y/%m/%d')

	def __str__(self):
		return self.user.username 

# post catgory
class Category(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)

	def __str__(self):
		return self.title 

# post list 
class Post(models.Model):
	category = models.ManyToManyField(Category,
										related_name='posts')
	author = models.ForeignKey(Author, related_name='author_posts',
								on_delete=models.CASCADE)
	title = 	models.CharField(max_length=200)
	content = HTMLField('Content')
	overview = 	models.TextField()
	image = 	models.ImageField(upload_to='posts/%Y/%m/%d')
	timestamp = models.DateTimeField(auto_now_add=True)
	previous_post = models.ForeignKey('self',related_name='previous',
													on_delete=models.SET_NULL, 
													null=True,
													blank=True)
	next_post = models.ForeignKey('self',related_name='next',
													on_delete=models.SET_NULL, 

													null=True,
													blank=True)

	def __str__(self):
		return self.title 


	def get_absolute_url(self):
		return reverse('post_detail', args=[self.id])

	@property
	def post_author_profile_picture(self):
		return self.author.profile_picture.url
	
	@property
	def get_post_comments(self):
		return self.comments.all().order_by('-timestamp')

	@property
	def post_view_count(self):
		return PostView.objects.filter(post=self).count()





	


# post comments  
class Comment(models.Model):
	user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, blank=True)
	email = models.EmailField(blank=True)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ('-timestamp',)

	def __str__(self):
		return self.user.username

# post view count 
class PostView(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)


