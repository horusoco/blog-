from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse 
from django.db.models  import Q
from django.core.paginator import Paginator, EmptyPage,\
									PageNotAnInteger

from .models import Post, Category, PostView
from marketing.forms  import SignupForm
from .forms import CommentForm

#first page 
def index(request):
	posts = Post.objects.all().order_by('-timestamp')[:3]
	
	if request.method == 'POST':
		signup_form = SignupForm(request.POST or None )
		if signup_form.is_valid():
			signup_form.save()
		
		
	else:
		signup_form = SignupForm()
		#NOTE SignupForm maynu gayn xaga htmlka 
	
	return render(request, 'index.html', 
								{'posts':posts,
								'signup_form':signup_form})

# blog post list 
def post_list(request):
	post_list = Post.objects.all()
	post_recent = Post.objects.all().order_by('-timestamp')[:3]
	post_categories = Category.objects.all()
	

	query = request.GET.get('q')
	if query:
		post_list = post_list.filter(
					Q(title__icontains=query)|
					Q(overview__icontains=query)
					).distinct()

	paginator = Paginator(post_list, 4) # 3 posts in each page

	page = request.GET.get('page')
	try:
		post_list = paginator.page(page)
		
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		post_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of results
		post_list = paginator.page(paginator.num_pages)

	return render(request, 'blog.html', {'post_list':post_list,
										'post_recent':post_recent,
										'post_categories':post_categories})


# blog post detail
def post_detail(request, id):
	post = get_object_or_404(Post, id=id)
	post_recent = Post.objects.all().order_by('-timestamp')[:3]
	post_categories = Category.objects.all()
	# userka viewga sameeyey iyo postada uu ku sameeyeey 
	PostView.objects.get_or_create(user=request.user, post=post)
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			comment_form.cleaned_data.get('content')
			comment_form.instance.post = post
			comment_form.instance.user = request.user
			comment_form.save()
			return redirect(reverse('post_detail', args=[post.id]))
					
	else:
		comment_form = CommentForm()

		

	return render(request, 'post_detail.html', {'post':post,
										'post_recent':post_recent,
										'post_categories':post_categories,
										'comment_form':comment_form})

 

# search posts 
def post_search(request):
	post_recent = Post.objects.all().order_by('-timestamp')[:5]
	post_categories = Category.objects.all()
	posts = Post.objects.all()
	query = request.GET.get('q')

	if query:
			posts = posts.filter(
			Q(title__icontains=query) |
			Q(overview__icontains=query)
			).distinct()

	context = {
	'posts': posts,
	'query':query,
	'post_recent':post_recent,
	'post_categories':post_categories
	}
	return render(request, 'post_search.html', context)

# posts in each category 

def category_posts(request, category_slug=None):
	categories = Category.objects.all()
	category = get_object_or_404(Category, slug=category_slug)
	category_posts = category.posts.all()

	context = {
		'category':category,
		'category_posts':category_posts,
		'categories':categories
	}
	return render(request, 'category_posts.html', context)


def contact(request):
	return render(request, 'contact.html', {})