
from assessments import Govtech
import argparse

def main():
    """
    main() to invoke data analyze functions.
    """
    
    parser = argparse.ArgumentParser(description="Restaurants data analyze script")
    parser.add_argument("--type", help="data type", required=True)
    parser.add_argument("--csv", help="csv file", required=True)
    parser.parse_args()
    args = parser.parse_args()
    
    if args.type and args.csv:
        gov = Govtech()

        restaurant_data = []

        if args.type == "events":
            restaurant_data = gov.my_restaurants_events()
        elif args.type == "data":
            restaurant_data = gov.get_restaurants()
        
        gov.export_to_csv(args.csv, restaurant_data)
    else:
        print("[usage] demo.py --type [Data type] --csv [CSV File Path]") 

if __name__ == "__main__":
    main()