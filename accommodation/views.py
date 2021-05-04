import json

from datetime               import datetime
from django.views           import View
from django.http            import JsonResponse, HttpResponse, Http404
from django.db.models       import Count, Min, Max
from django.db.models       import Q

from user.models            import User
from accommodation.models   import (
    Accommodation,
    AccommodationImage,
    Category,
    Address,
    City,
    Host,
    Room,
    RoomOption,
    Review,
    Option,
    UnavailableDate
)

class AccommodationListView(View):

    def get(self, request, category_id=0):
        try:

            """
            Created: 2021-03-09
            Updated: 2021-05-04
            
            [숙소 리스트 페이지]
            - 도시, 체크인 날짜, 체크아웃 날짜, 인원, 평점, 룸 옵션 필터 기능
            - 정렬 기능

            ~ 도시(city)
            - 한글 형식

            ~ 체크인 날짜(startDate), 체크아웃 날짜(endDate)
            - YYYY-MM-DD 형식

            ~ 인원(guest)
            - 입력된 int 보다 같거나 많은 인원 수용 가능 숙소

            ~ 평점(rate)
            - 입력된 int 보다 같거나 높은 평점 숙소

            ~ 룸 옵션(roomOption)
            - 1~30가지

            ~ 정렬(ordering)
            - favored(추천순)
            - ratingHigh(평점순)
            - priceLow(가격낮은순)
            - priceHigh(가격높은순)
            """

            city         = request.GET['city']
            start_date   = request.GET['startDate']
            end_date     = request.GET['endDate']
            guest        = request.GET['guest']
            ordering     = request.GET.get('order', 'favored')
            rate         = request.GET.get('rate', 0.00)
            room_option  = request.GET.getlist('roomOption', None)

            q = (Q(city__name=city)
                & Q(room__maximum_capacity__gte=guest)
                & Q(rate__gte=rate)
                & ~Q(room__unavailabledate__start_date__gte=start_date, room__unavailabledate__end_date__lte=end_date)
            )

            if category_id:
                q &= Q(category__id=category_id)

            accommodations = Accommodation.objects\
                .select_related('address','category','city')\
                .prefetch_related('accommodationimage_set','room_set','review_set')\
                .filter(q)\
                .annotate(count=Count('review'), price=Min('room__price'))

            if room_option:
                for r in room_option:
                    accommodations = accommodations.filter(room__option__name=r)

            ordering_options = {
                'favored' : '-count',
                'ratingHigh' : '-rate',
                'priceLow' : 'price',
                'priceHigh' : '-price'
            }

            data = [
                {
                    'id'          : accommodation.id,
                    'name'        : accommodation.name,
                    'description' : accommodation.description,
                    'category'    : accommodation.category.name,
                    'rate'        : accommodation.rate,
                    'review'      : accommodation.count,
                    'price'       : accommodation.price,
                    'url'         : accommodation.accommodationimage_set.all()[0].image_url,
                } for accommodation in accommodations.order_by(ordering_options[ordering])
            ]

            return JsonResponse({'data': data}, status=200)

        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)

class AccommodationDetailView(View):
    def get(self, request, accommodation_id):
        try:

            """
            Created: 2021-03-09
            Updated: 2021-05-04
            
            [숙소 상세 페이지]
            - 숙소 상세 정보 확인 기능
            - 리뷰 확인 기능 
            """

            accommodation = Accommodation.objects.get(id=accommodation_id)
            review_count  = Review.objects.filter(accommodation=accommodation_id).count()
            
            data = {
                'id'            : accommodation.id,
                'name'          : accommodation.name,
                'description'   : accommodation.description,
                'total_rate'    : accommodation.rate,
                'review_number' : review_count,
                'room'          : [{
                    'name'           : room.name,
                    'price'          : room.price,
                    'basic_capacity' : room.basic_capacity,
                    'max_capacity'   : room.maximum_capacity,
                    'image'          : [
                        {
                            'image_url' : image.image_url 
                        } for image in room.accommodation.accommodationimage_set.all()
                    ],
                } for room in accommodation.room_set.all()],
                'main_image'    : accommodation.accommodationimage_set.first().image_url,
                'address'       : accommodation.address.name,
                'host'          : {
                    'name'           : accommodation.host.name,
                    'image_url'      : accommodation.host.image_url
                },
                'review_list'   : [
                    {
                        'user'        : review.user.nickname,
                        'created_at'  : review.created_at,
                        'content'     : review.content,
                        'total_rate'  : review.total_rate
                    } for review in accommodation.review_set.all()
                ]
            }

            return JsonResponse({'data': data}, status=200)

        except Accommodation.DoesNotExist:
            return JsonResponse({'message': 'INVALID_ACCOMMODATION_ID'}, status=404)