import os
import sys
import itertools
import api
import datetime
from .models import Favorite
import datetime as dt
import pandas as pd
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.db.models import Avg


sys.path.append("../")
from standbytime.models import standbyTimeDataTDL, standbyTimeDataTDS

# Create your views here.


def dataMerge(request, park_type):
    if park_type == "TDL":
        parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
        favorites = pd.DataFrame(
            Favorite.objects.filter(user_id=request.user.id, park_type="TDL")
            .order_by("facilityCode")
            .values("facilityCode", "submit_time")
        )
        try:
            avgDatas = pd.DataFrame(
                standbyTimeDataTDL.objects.filter(
                    time__range=[
                        (timezone.now() + dt.timedelta(days=-22)).strftime("%Y-%m-%d"),
                        timezone.now().strftime("%Y-%m-%d"),
                    ],
                    time__icontains=timezone.now().strftime("%H:%M"),
                )
                .values("facilityCode")
                .order_by("facilityCode")
                .annotate(average=Avg("standby_time"))
            )
        except:
            pass
    else:
        parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
        favorites = pd.DataFrame(
            Favorite.objects.filter(user_id=request.user.id, park_type="TDS")
            .order_by("facilityCode")
            .values("facilityCode", "submit_time")
        )
        try:
            avgDatas = pd.DataFrame(
                standbyTimeDataTDL.objects.filter(
                    time__range=[
                        (timezone.now() + dt.timedelta(days=-22)).strftime("%Y-%m-%d"),
                        timezone.now().strftime("%Y-%m-%d"),
                    ],
                    time__icontains=timezone.now().strftime("%H:%M"),
                )
                .values("facilityCode")
                .order_by("facilityCode")
                .annotate(average=Avg("standby_time"))
            )
        except:
            pass
    facilitys = pd.DataFrame(list(api.get_facilities()["attractions"]))
    facilitys_conditions = pd.DataFrame(
        list(api.get_facilities_conditions()["attractions"])
    )
    facilitys_pd = pd.merge(
        facilitys, facilitys_conditions, on="facilityCode", how="left",
    )
    try:
        facilitys_pd = facilitys_pd.merge(favorites, on="facilityCode", how="left")
    except:
        pass
    try:
        facilitys_pd = facilitys_pd.merge(avgDatas, on="facilityCode", how="left")
    except:
        pass
    try:
        facilitys_pd["vacant"] = facilitys_pd["average"] > facilitys_pd["standbyTime"]
    except:
        facilitys_pd["vacant"] = False
    # NaNをNoneに置換
    facilitys_pd = facilitys_pd[facilitys_pd["parkType"] == park_type]
    facilitys_pd = facilitys_pd.astype(object).where((pd.notnull(facilitys_pd)), None)
    return parks_condition, facilitys_pd


class OverView(View):
    def get(self, request, park_type):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
                attractions_overview = {
                    standby_time["facilityCode"]: standby_time["standby_time_avg"]
                    if standby_time["standby_time_avg"]
                    else -1
                    for standby_time in standbyTimeDataTDL.objects.filter(
                        time__startswith=timezone.now().date()
                    )
                    .select_related()
                    .values("facilityCode")
                    .order_by("facilityCode")
                    .annotate(standby_time_avg=Avg("standby_time"))
                }
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
                attractions_overview = {
                    standby_time["facilityCode"]: standby_time["standby_time_avg"]
                    if standby_time["standby_time_avg"]
                    else -1
                    for standby_time in standbyTimeDataTDS.objects.filter(
                        time__startswith=timezone.now().date()
                    )
                    .select_related()
                    .values("facilityCode")
                    .order_by("facilityCode")
                    .annotate(standby_time_avg=Avg("standby_time"))
                }
            attractions = sorted(
                api.get_facilities()["attractions"], key=lambda x: x["facilityCode"]
            )
            attractions_conditions = sorted(
                api.get_facilities_conditions()["attractions"],
                key=lambda x: x["facilityCode"],
            )

            f_attractions = []
            for i, attraction in enumerate(attractions):
                if attraction["parkType"] == park_type:
                    attractions[i].update(attractions_conditions[i])
                    attractions[i].update(
                        {"avg": attractions_overview[int(attraction["facilityCode"])]}
                    )
                    f_attractions.append(attraction)
            f_attractions.sort(reverse=True, key=lambda x: (x["avg"], x["name"]))

            return render(
                request,
                "information/overview.html",
                {
                    "attractions": f_attractions,
                    "park_type": park_type,
                    "parks_condition": parks_condition,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class AttractionList(View):
    def get(self, request, park_type):
        try:
            parks_condition, attractions_pd = dataMerge(request, park_type)
            attractions = attractions_pd.to_dict(orient="records")
            attractions.sort(key=lambda x: (x["area"]["id"], x["name"]))
            attraction_groups = {
                area: list(data)
                for area, data in itertools.groupby(
                    attractions, lambda x: x["area"]["id"]
                )
            }
            return render(
                request,
                "information/attractionlist.html",
                {
                    "attraction_groups": attraction_groups,
                    "park_type": park_type,
                    "now_open_info": parks_condition,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")

    def post(self, request, park_type):
        if "facility_code_off" in request.POST:
            Favorite.objects.create(
                user_id=request.user.id,
                park_type=park_type,
                facilityCode=request.POST["facility_code_off"],
            )
        else:
            Favorite.objects.filter(
                facilityCode=request.POST["facility_code_on"]
            ).delete()
        return redirect("information:attractionlist", park_type)


class AttractionDetail(View):
    def get(self, request, park_type, facility_code):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            attractions = pd.DataFrame(list(api.get_facilities()["attractions"]))
            attractions_conditions = pd.DataFrame(
                list(api.get_facilities_conditions()["attractions"])
            )
            attractions_pd = pd.merge(
                attractions, attractions_conditions, on="facilityCode", how="left",
            )
            attraction_pd = attractions_pd[
                attractions_pd["facilityCode"] == facility_code
            ]
            attraction_pd = attraction_pd.astype(object).where(
                (pd.notnull(attraction_pd)), None
            )
            attraction = attraction_pd.to_dict(orient="records")[0]
            if park_type == "TDL":
                data_ = len(
                    [
                        1
                        for i in standbyTimeDataTDL.objects.filter(
                            time__startswith=timezone.now().date(),
                            facilityCode=facility_code,
                        )
                        if i.standby_time != None
                    ]
                )
            else:
                data_ = len(
                    [
                        1
                        for i in standbyTimeDataTDS.objects.filter(
                            time__startswith=timezone.now().date(),
                            facilityCode=facility_code,
                        )
                        if i.standby_time != None
                    ]
                )
            try:
                attraction["operatings"][0]["startAt"] = datetime.datetime.strptime(
                    attraction["operatings"][0]["startAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ) + datetime.timedelta(hours=9)
                attraction["operatings"][0]["endAt"] = datetime.datetime.strptime(
                    attraction["operatings"][0]["endAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ) + datetime.timedelta(hours=9)
                pass
            except:
                pass
            return render(
                request,
                "information/attractiondetail.html",
                {
                    "now_open_info": parks_condition,
                    "park_type": park_type,
                    "attraction_groups": attraction,
                    "data_": data_,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class FavoriteAttractionList(View):
    def get(self, request, park_type):
        if Favorite.objects.filter(user_id=request.user.id).exists():
            try:
                parks_condition, attractions_pd = dataMerge(request, park_type)
                attractions_pd = attractions_pd[
                    pd.isna(attractions_pd["submit_time"]) != True
                ]
                attractions = attractions_pd[
                    attractions_pd["parkType"] == park_type
                ].to_dict(orient="records")
                attractions.sort(key=lambda x: (x["area"]["id"], x["name"]))
                attraction_groups = {
                    area: list(data)
                    for area, data in itertools.groupby(
                        attractions, lambda x: x["area"]["id"]
                    )
                }
                return render(
                    request,
                    "information/favoriteattractionlist.html",
                    {
                        "attraction_groups": attraction_groups,
                        "park_type": park_type,
                        "now_open_info": parks_condition,
                        "weatherData": api.getWeather(),
                    },
                )
            except:
                return redirect("error")
        else:
            return render(
                request,
                "information/favoriteattractionlist.html",
                {"weatherData": api.getWeather(),},
            )

    def post(self, request, park_type):
        Favorite.objects.filter(facilityCode=request.POST["facility_code_on"]).delete()
        return redirect("information:favoriteattractionlist", park_type)


class AttractionMap(View):
    def get(self, request, park_type, facility_code):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            attractions = api.get_facilities()["attractions"]
            for attraction in attractions:
                if attraction["facilityCode"] == facility_code:
                    info = attraction
                    break
            try:
                map_key = os.environ["GOOGLEMAPAPI_KEY"]
            except KeyError:
                import local_api

                map_key = local_api.google_map_api_key()
            return render(
                request,
                "information/map.html",
                {
                    "map_key": map_key,
                    "now_open_info": parks_condition,
                    "park_type": park_type,
                    "info": info,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class RestaurantList(View):
    def get(self, request, park_type):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            restaurants = pd.DataFrame(list(api.get_facilities()["restaurants"]))
            restaurants_conditions = pd.DataFrame(
                list(api.get_facilities_conditions()["restaurants"])
            )
            restaurants_pd = pd.merge(
                restaurants, restaurants_conditions, on="facilityCode", how="left",
            )
            restaurants_pd = restaurants_pd[restaurants_pd["parkType"] == park_type]
            restaurants_pd = restaurants_pd.astype(object).where(
                (pd.notnull(restaurants_pd)), None
            )
            restaurants = restaurants_pd.to_dict(orient="records")
            restaurants.sort(key=lambda x: (x["area"]["id"], x["name"]))
            restaurant_groups = {
                area: list(data)
                for area, data in itertools.groupby(
                    restaurants, lambda x: x["area"]["id"]
                )
            }
            return render(
                request,
                "information/restaurantlist.html",
                {
                    "restaurant_groups": restaurant_groups,
                    "park_type": park_type,
                    "now_open_info": parks_condition,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class RestaurantDetail(View):
    def get(self, request, park_type, facility_code):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            restaurants = pd.DataFrame(list(api.get_facilities()["restaurants"]))
            restaurants_conditions = pd.DataFrame(
                list(api.get_facilities_conditions()["restaurants"])
            )
            restaurants_pd = pd.merge(
                restaurants, restaurants_conditions, on="facilityCode", how="left",
            )
            restaurant_pd = restaurants_pd[
                restaurants_pd["facilityCode"] == facility_code
            ]
            restaurant_pd = restaurant_pd.astype(object).where(
                (pd.notnull(restaurants_pd)), None
            )
            restaurant = restaurant_pd.to_dict(orient="records")[0]
            try:
                restaurant["operatings"][0]["startAt"] = datetime.datetime.strptime(
                    restaurant["operatings"][0]["startAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ) + datetime.timedelta(hours=9)
                restaurant["operatings"][0]["endAt"] = datetime.datetime.strptime(
                    restaurant["operatings"][0]["endAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ) + datetime.timedelta(hours=9)
                pass
            except:
                pass
            return render(
                request,
                "information/restaurantdetail.html",
                {
                    "now_open_info": parks_condition,
                    "park_type": parks_condition,
                    "restaurant": restaurant,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class RestaurantMap(View):
    def get(self, request, park_type, facility_code):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            restaurants = api.get_facilities()["restaurants"]
            for restaurant in restaurants:
                if restaurant["facilityCode"] == facility_code:
                    info = restaurant
                    break
            try:
                map_key = os.environ["GOOGLEMAPAPI_KEY"]
            except KeyError:
                import local_api

                map_key = local_api.google_map_api_key()
            return render(
                request,
                "information/map.html",
                {
                    "map_key": map_key,
                    "now_open_info": parks_condition,
                    "park_type": park_type,
                    "info": info,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class ShopList(View):
    def get(self, request, park_type):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            shops = sorted(
                api.get_facilities()["shops"], key=lambda x: x["facilityCode"],
            )
            shops_conditions = sorted(
                api.get_facilities_conditions()["shops"],
                key=lambda x: x["facilityCode"],
            )
            f_shops = []
            for i, shop in enumerate(shops):
                if shop["parkType"] == park_type:
                    shops[i].update(shops_conditions[i])
                    f_shops.append(shop)
            f_shops.sort(key=lambda x: (x["area"]["id"], x["name"]))
            shop_groups = {
                area: list(data)
                for area, data in itertools.groupby(f_shops, lambda x: x["area"]["id"])
            }
            return render(
                request,
                "information/shoplist.html",
                {
                    "shop_groups": shop_groups,
                    "park_type": park_type,
                    "now_open_info": parks_condition,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class ShopDetail(View):
    def get(self, request, shop_name, park_type, facility_code):
        try:
            shops = sorted(
                api.get_facilities()["shops"], key=lambda x: x["facilityCode"],
            )
            shops_conditions = sorted(
                api.get_facilities_conditions()["shops"],
                key=lambda x: x["facilityCode"],
            )
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            for i, shop in enumerate(shops):
                if shop["name"] == shop_name:
                    shops[i].update(shops_conditions[i])
                    info = shops[i]
                    try:
                        info["operatings"][0]["startAt"] = datetime.datetime.strptime(
                            info["operatings"][0]["startAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ) + datetime.timedelta(hours=9)
                        info["operatings"][0]["endAt"] = datetime.datetime.strptime(
                            info["operatings"][0]["endAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ) + datetime.timedelta(hours=9)
                    except:
                        pass
                    break
            return render(
                request,
                "information/shopdetail.html",
                {
                    "now_open_info": parks_condition,
                    "park_type": parks_condition,
                    "info": info,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class ShopMap(View):
    def get(self, request, park_type, facility_code):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            shops = api.get_facilities()["shops"]
            for shop in shops:
                if shop["facilityCode"] == facility_code:
                    info = shop
                    break
            try:
                map_key = os.environ["GOOGLEMAPAPI_KEY"]
            except KeyError:
                import local_api

                map_key = local_api.google_map_api_key()
            return render(
                request,
                "information/map.html",
                {
                    "map_key": map_key,
                    "now_open_info": parks_condition,
                    "park_type": park_type,
                    "info": info,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")


class ServiceSpotList(View):
    def get(self, request, park_type):
        try:
            if park_type == "TDL":
                parks_condition = api.get_parks_conditions()["schedules"][0]["open"]
            else:
                parks_condition = api.get_parks_conditions()["schedules"][1]["open"]
            servicespots = sorted(
                api.get_facilities()["serviceSpots"], key=lambda x: x["facilityCode"],
            )
            dellists = []
            for i, servicespot in enumerate(servicespots):
                if "OUTSIDE_PARK" in servicespot["filters"]:
                    dellists.append(i)
            i = 0
            for dellist in dellists:
                del servicespots[dellist - i]
                i += 1
            servicespots.sort(key=lambda x: (x["area"]["id"], x["name"]))
            servicespot_groups = {
                area: list(data)
                for area, data in itertools.groupby(
                    servicespots, lambda x: x["area"]["id"]
                )
            }
            return render(
                request,
                "information/servicespotlist.html",
                {
                    "servicespot_groups": servicespot_groups,
                    "park_type": park_type,
                    "now_open_info": parks_condition,
                    "weatherData": api.getWeather(),
                },
            )
        except:
            return redirect("error")

