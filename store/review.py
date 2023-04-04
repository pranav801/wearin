from django.shortcuts import redirect, render
from .models import ReviewRating
from store.forms import ReviewForm
from django.contrib import messages
from admin_home.views import superadmin_check
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


# review rating-------------
@login_required(login_url = 'login')
def submit_review(request, product_id):

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':

        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.image = request.FILES.get('image')
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')

                return redirect(url)


# def editReview(request,review_id):


@login_required(login_url = 'login')
def deleteReview(request, id):
    url = request.META.get('HTTP_REFERER')
    del_review = ReviewRating.objects.filter(id=id)
    del_review.delete()

    return redirect(url)



#--------review mangement by admin -----------

@user_passes_test(superadmin_check)
def review_management(request):
    reviews = ReviewRating.objects.all()
    return render(request, 'adminhome/review_management.html', {'reviews' : reviews})

@user_passes_test(superadmin_check)
def remove_review(request, id):
    try:
        review = ReviewRating.objects.get(id=id)
        review.delete()
        messages.success(request, 'Review removed succesfully')
        return redirect(review_management)
    except ReviewRating.DoesNotExist:
        messages.warning(request, 'Oops!Something went wrong')
        return redirect(review_management)