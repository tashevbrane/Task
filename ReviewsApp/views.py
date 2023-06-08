import json
from django.shortcuts import render
from .models import Review


def filter_reviews(request):
    if request.method == 'GET':
        prioritize_text = request.GET.get('prioritize_text', 'No')
        rating_order = request.GET.get('rating_order', 'Highest First')
        date_order = request.GET.get('date_order', 'Oldest First')
        min_rating = int(request.GET.get('min_rating', 1))
    else:
        prioritize_text = request.POST.get('prioritize_text', 'No')
        rating_order = request.POST.get('rating_order', 'Highest First')
        date_order = request.POST.get('date_order', 'Oldest First')
        min_rating = int(request.POST.get('min_rating', 1))

    with open('data/reviews.json') as file:
        reviews_data = json.load(file)

    reviews = []
    for review_data in reviews_data:
        review = Review(
            text=review_data['reviewText'],
            rating=review_data['rating'],
            date=review_data['reviewCreatedOnDate']
        )
        reviews.append(review)

    filtered_reviews = [review for review in reviews if review.rating >= min_rating]

    if prioritize_text == 'Yes':
        reviews_with_text = [review for review in filtered_reviews if review.text]
        reviews_without_text = [review for review in filtered_reviews if not review.text]

        sorted_reviews_with_text = sorted(reviews_with_text,
                                          key=lambda x: (x.rating, x.date) if date_order == 'Oldest First' else (
                                          x.rating, -x.date))
        sorted_reviews_without_text = sorted(reviews_without_text,
                                             key=lambda x: (x.rating, x.date) if date_order == 'Oldest First' else (
                                             x.rating, -x.date))

        filtered_and_sorted_reviews = sorted_reviews_with_text + sorted_reviews_without_text
    else:
        filtered_and_sorted_reviews = sorted(filtered_reviews,
                                             key=lambda x: (x.rating, x.date) if date_order == 'Oldest First' else (
                                             x.rating, -x.date))

    context = {'reviews': filtered_and_sorted_reviews}
    return render(request, 'filter.html', context)
