
from assessments import Govtech
import argparse

def main():
    """
    main() to invoke data analyze functions.
    """
    
    gov = Govtech()
    gov.analyze()

if __name__ == "__main__":
    main()