def get_rating_percentage(queryset):
    total_rating = queryset.count() * 5
    if total_rating != 0:
        sum_rating = 0
        for review in queryset:
            sum_rating += int(review.rating)
        rating_percentage = ( sum_rating / total_rating ) * 100
        return rating_percentage
    else:
        return 0