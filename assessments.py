
import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import json
import csv

class Govtech(object):

    def __init__(self):
        self.restaurant_data_url = "https://raw.githubusercontent.com/ashraf356/cc4braininterview/main/restaurant_data.json"
        self.restaurant_json_file = "restaurant_data.json"
    
    def __get_country_name(self, latitude, longitude, country, shelf):
        country_id = "{0}".format(country)
        
        if country_id in shelf:
            return shelf[country_id]
        
        geolocator = Nominatim(user_agent="geoapiExercises", timeout=3)

        location = geolocator.reverse("{0},{1}".format(latitude, longitude), language='en')
        
        if location:
            address = location.raw['address']
            if address.get('country'): shelf[country_id] = address.get('country', 'NA')
            return address.get('country', 'NA')
        
        return 'NA'

    def export_to_csv(self, file, data):
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in data:
                writer.writerow(i)

    def get_restaurants(self):
        """
        get_restaurants() process restaurant data
        """

        with requests.Session() as session:
            session.headers.update({'Content-type': 'application/json'})
            session.headers.update({'Accept': 'application/json'})

            response = session.get(self.restaurant_data_url)

            restaurants_csv = []
            shelf = {}

            if response.status_code == 200:
                restaurants_data = response.json()
                
                print("Total restaurants: {0}".format(len(restaurants_data)))
                print("Restauntant Name,Restauntant ID,Country,City,Aggregate Rating,Votes,Cuisines")
                restaurants_csv.append("Restauntant Name,Restauntant ID,Country,City,Aggregate Rating,Votes,Cuisines"
                    .split(","))

                for rd in restaurants_data:
                    if "restaurants" in rd:
                        restaurants = rd["restaurants"]
                        
                        for r in restaurants:
                            restaurant = r["restaurant"]
                            country_name = self.__get_country_name(
                                restaurant["location"]["latitude"],
                                restaurant["location"]["longitude"],
                                restaurant["location"]["country_id"],
                                shelf
                            )
                            print("{0},{1},{2},{3},{4},{5},{6}".format(
                                restaurant["name"],
                                restaurant["id"],
                                country_name,
                                restaurant["location"]["city"],
                                restaurant["user_rating"]["aggregate_rating"],
                                restaurant["user_rating"]["votes"],
                                restaurant["cuisines"]
                            ))
                            
                            restaurants_csv.append([
                                restaurant["name"],
                                restaurant["id"],
                                country_name,
                                restaurant["location"]["city"],
                                restaurant["user_rating"]["aggregate_rating"],
                                restaurant["user_rating"]["votes"],
                                restaurant["cuisines"]
                            ])
            else:
                print(response.text)
            
            return restaurants_csv

    def my_restaurants_events(self):
        """
        my_restaurants_events() restaurants events
        """

        with open(self.restaurant_json_file, "r") as jf:
            restaurants_data = json.load(jf)

            restaurants_csv = []

            if restaurants_data:
                print("Total restaurants: {0}".format(len(restaurants_data)))
                print("Event ID,Restauntant ID,Restauntant Name,Event Title,Event Start Date,Event End Date,Photo Url")
                restaurants_csv.append("Event ID,Restauntant ID,Restauntant Name,Event Title,Event Start Date,Event End Date,Photo Url"
                    .split(","))

                for rd in restaurants_data:
                    if "restaurants" in rd:
                        restaurants = rd["restaurants"]

                        for r in restaurants:
                            restaurant = r["restaurant"]
                            
                            # print(restaurant)

                            if "zomato_events" in restaurant:
                                for e in restaurant["zomato_events"]:
                                    # print("event >>> ", e)

                                    photos = []
                                    for p in e["event"]["photos"]:
                                        photos.append(p["photo"]["url"])
                                        # print("photo url: ", p["photo"]["url"])
                                    
                                    photostr = " ".join(photos)
                                    if len(photos) == 0:
                                        photostr = "NA"
                                    
                                    start_date = datetime.strptime(e["event"]["start_date"], "%Y-%m-%d")
                                    end_date = datetime.strptime(e["event"]["end_date"], "%Y-%m-%d")
                                    
                                    if start_date.year == 2017 and start_date.month == 4 and end_date.year == 2017 and end_date.month == 4:
                                        print("{0},{1},{2},{3},{4},{5},{6}".format(
                                            e["event"]["event_id"],
                                            restaurant["id"],
                                            restaurant["name"],
                                            e["event"]["title"],
                                            e["event"]["start_date"],
                                            e["event"]["end_date"],
                                            photostr
                                        ))
                                        
                                        restaurants_csv.append([
                                            e["event"]["event_id"],
                                            restaurant["id"],
                                            restaurant["name"],
                                            e["event"]["title"],
                                            e["event"]["start_date"],
                                            e["event"]["end_date"],
                                            photostr
                                        ])
            
            return restaurants_csv

    def analyze(self):
        """
        analyze() rating text
        """
        aggr_map = {}
        with open(self.restaurant_json_file, "r") as jf:
            restaurants_data = json.load(jf)

            if restaurants_data:
                print("Total restaurants: {0}".format(len(restaurants_data)))

                for rd in restaurants_data:
                    if "restaurants" in rd:
                        restaurants = rd["restaurants"]
                        
                        for r in restaurants:
                            restaurant = r["restaurant"]
                            
                            # print(restaurant)

                            rating_text = restaurant["user_rating"]["rating_text"]

                            aggr_rating = restaurant["user_rating"]["aggregate_rating"]

                            if rating_text in aggr_map:
                                aggr_ratings = aggr_map[rating_text]
                                aggr_ratings.append(aggr_rating)
                                aggr_map[rating_text] = aggr_ratings
                            else:
                                aggr_map[rating_text] = [aggr_rating]

        print("Ratings aggregate:")
        
        # print("aggr_map: ", aggr_map)
        
        for rating in aggr_map:
            aggr_values = aggr_map[rating]
            
            aggr_length = len(aggr_values)
            
            aggr_sum = 0
            for i in aggr_values:
                aggr_sum += float(i)
            
            aggr_rate = aggr_sum * 100 / (aggr_length * 100)
            print(rating,":", aggr_rate)