import json

from django.http        import JsonResponse
from django.views       import View

from .models      import Airline, Airport, FlightPrice, FlightSchedule, FlightStatus

class FlightView(View):
    def get(self, request):
        try:

            """
            Created: 2021-03-09
            Updated: 2021-05-04

            http://localhost:8000/flight?date=2021-03-12&departure=GMP&arrival=CJU&passenger=2&sort=price:asc&timeOption=1
            
            [항공 페이지]
            - 출발지, 도착지, 날짜, 시간대, 인원 필터 기능
            - 정렬 기능

            ~ 출발지(arrival)
            - 영어 세글자 code

            ~ 도착지(departure)
            - 영어 세글자 code

            ~ 날짜(date)
            - YYYY-MM-DD

            ~ 시간대(time_option)
            - 1(새벽 00:00~06:00)
            - 2(오전 06:00~12:00)
            - 3(오후 12:00~18:00)
            - 4야간 18:00~24:00)

            ~ 인원(passenger)
            - int

            """

            data        = request.GET
            arrival     = data['arrival']
            date        = data['date']
            departure   = data['departure']
            sort        = data['sort']
            time_option = data.getlist('timeOption')
            passenger   = data['passenger']

            flights = FlightSchedule.objects.select_related(
                'departure_airport',
                'arrival_airport',
                'airline').filter(
                departure_airport__code=departure,
                arrival_airport__code=arrival,
                departure_date=date,
                ).filter(
                    time_frame__in=time_option,
                    flight_prices__remaining_seat__gte=passenger,
                )

            sort_option = {
                'departureTime:asc'  : 'departure_time',
                'departureTime:desc' : '-departure_time',
                'price:asc'          : 'flight_prices__price'
            }

            flight_info = [{
                'id'            : flight.id,
                'airline'       : flight.airline.name,
                'airline_logo'  : flight.airline.image_url,
                'flightCode'    : flight.flight_code,
                'departureTime' : flight.departure_time,
                'arrivalTime'   : flight.arrival_time,
                'durationTime'  : flight.duration_time,
                'status'        : flight.flight_prices.get().status.name,
                'remainingSeat' : flight.flight_prices.get().remaining_seat,
                'price'         : flight.flight_prices.get().price
            } for flight in flights.order_by(sort_option[sort])]

            return JsonResponse({
                'date'                 : date,
                'departureAirportName' : flights[0].departure_airport.name,
                'departureAirportCode' : departure,
                'arrivalAirportName'   : flights[0].arrival_airport.name,
                'arrivalAirportCode'   : arrival,
                'flights'              : flight_info
            }, status=200)
        
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except IndexError:
            return JsonResponse({
                'message'              : 'INDEX_ERROR',
                'date'                 : date,
                'departureAirportCode' : departure,
                'arrivalAirportCode'   : arrival,
                }, status=400)
