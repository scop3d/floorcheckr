import me_api.constants as constants
import json
import requests
import time
import urllib3
from me_api.utils import Utils


http = urllib3.PoolManager()


class Collections:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.all_listings = self.all_listings()

    ###########################COLLECTIONS##########################
    def all_projects(self) -> dict:
        output = []
        offset = 0
        while True:
            resp = json.loads(
                http.request(
                    "GET", f"{constants.HOST}/collections?offset={offset}&limit=500"
                ).data
            )
            if len(resp) == 0:
                return output
            else:
                for obj in resp:
                    output.append(obj)
                offset += 500

    # returns metadata about a project
    def project_details(self) -> list:
        resp = json.loads(
            http.request("GET", f"{constants.HOST}/collections/{self.symbol}").data
        )
        return resp

        # https://api-mainnet.magiceden.io/rpc/getCollectionsWithSymbols?symbols=[%22the_remnants_%22]&edge_cache=true
        # return filter(lambda project: self.symbol.lower() in project['symbol'].lower(), self.all_projects)

    # returns listings for a project
    def all_listings(self) -> list:
        output = []
        offset = 0
        while True:
            resp = json.loads(
                http.request(
                    "GET",
                    f"{constants.HOST}/collections/{self.symbol}/listings?offset={offset}&limit=20",
                ).data
            )
            if len(resp) == 0:
                return output
            else:
                for obj in resp:
                    output.append(obj)
                offset += 20

    # returns listings for a project
    def get_max_listing_price(self) -> list:
        listings = self.all_listings
        return max(listings, key=lambda x: x["price"])["price"]

    # returns average listing price
    def get_average_listing_price(self) -> list:
        listings = self.all_listings
        total = sum(map(lambda x: x["price"], listings))
        count = len(listings)
        return total / count

    # returns median listing price
    def get_median_listing_price(self):
        listings = self.all_listings
        return Utils.median(list(map(lambda x: x["price"], listings)))

    # sort = ["count", "price"]]
    def get_price_distribution(self, sort: str = "count"):
        listings = self.all_listings
        return (
            Utils.count(list(map(lambda x: x["price"], listings)))
            if sort.lower() == "count"
            else dict(
                sorted(Utils.count(list(map(lambda x: x["price"], listings))).items())
            )
        )

    # returns list of sellers sorted by # of listed
    def get_sellers_distribution(self) -> dict:
        listings = self.all_listings
        return dict(
            sorted(Utils.count(list(map(lambda x: x["seller"], listings))).items())
        )

    # returns activities for a project
    def activities(self) -> list:
        output = []
        offset = 0
        while True:
            resp = json.loads(
                http.request(
                    "GET",
                    f"{constants.HOST}/collections/{self.symbol}/activities?offset={offset}&limit=500",
                ).data
            )
            if len(resp) == 0:
                return output
                break
            else:
                for obj in resp:
                    output.append(obj)
                offset += 500

    # returns listings for a project
    def get_sale_activities(self) -> list:
        output = []
        offset = 0
        while True:
            resp = json.loads(
                http.request(
                    "GET",
                    f"{constants.HOST}/collections/{self.symbol}/activities?offset={offset}&limit=500",
                ).data
            )
            if len(resp) == 0:
                return output
                break
            else:
                for obj in resp:
                    if obj["type"] == "buyNow":
                        output.append(obj)
                offset += 500

    def get_bid_activities(self) -> list:
        output = []
        offset = 0
        while True:
            resp = json.loads(
                http.request(
                    "GET",
                    f"{constants.HOST}/collections/{self.symbol}/activities?offset={offset}&limit=500",
                ).data
            )
            if len(resp) == 0:
                return output
                break
            else:
                for obj in resp:
                    if obj["type"] == "bid":
                        output.append(obj)
                offset += 500

    def get_list_activites(self) -> list:
        output = []
        offset = 0
        while True:
            resp = json.loads(
                http.request(
                    "GET",
                    f"{constants.HOST}/collections/{self.symbol}/activities?offset={offset}&limit=500",
                ).data
            )
            if len(resp) == 0:
                return output
            else:
                for obj in resp:
                    if obj["type"] == "list":
                        output.append(obj)
                offset += 500

    def get_delist_activites(self) -> list:
        output = []
        offset = 0
        while True:
            resp = json.loads(
                http.request(
                    "GET",
                    f"{constants.HOST}/collections/{self.symbol}/activities?offset={offset}&limit=500",
                ).data
            )
            if len(resp) == 0:
                return output
                break
            else:
                for obj in resp:
                    if obj["type"] == "delist":
                        output.append(obj)
                offset += 500

    ##############################STATS###############################
    def stats(self) -> dict:
        resp = json.loads(
            http.request(
                "GET", f"{constants.HOST}/collections/{self.symbol}/stats"
            ).data
        )
        return resp

    def get_listed_count(self) -> int:
        resp = json.loads(
            http.request(
                "GET", f"{constants.HOST}/collections/{self.symbol}/stats"
            ).data
        )["listedCount"]
        return resp

    def get_floor_price(self, unit: str = "sol") -> float:
        Utils.validate_unit(unit)
        resp = json.loads(
            http.request(
                "GET", f"{constants.HOST}/collections/{self.symbol}/stats"
            ).data
        )["floorPrice"]
        return resp if unit == "lamports" else Utils.lamports_to_sol(resp)

    # unit = ["sol", "lamports"]
    def get_total_volume(self, unit: str = "sol") -> float:
        Utils.validate_unit(unit)
        resp = json.loads(
            http.request(
                "GET", f"{constants.HOST}/collections/{self.symbol}/stats"
            ).data
        )["volumeAll"]
        return resp if unit == "lamports" else Utils.lamports_to_sol(resp)

    def get_daily_volume(self, unit: str = "sol") -> float:
        Utils.validate_unit(unit)
        resp = json.loads(
            http.request(
                "GET", f"{constants.HOST}/collections/{self.symbol}/stats"
            ).data
        )["avgPrice24hr"]
        return resp if unit == "lamports" else Utils.lamports_to_sol(resp)

    def listing_info(self):
        output = f"""
                {self.symbol}
                Number Listed: {self.get_listed_count()}
                Floor Price: {round(self.get_floor_price(),2)}
                Average Listing Price: {round(self.get_average_listing_price(),2)}
                Median Listing Price: {round(self.get_median_listing_price(),2)}
                Max Listing Price: {round(self.get_max_listing_price(),2)}
                Avg 24 Hour Volume: {round(self.get_average_daily_volume(),2)}
                Total Volume: {round(self.get_total_volume(),2)}
                """
        return output

    def listing_data(self):
        output = {
            "symbol": self.symbol,
            "floor_price": round(self.get_floor_price(), 2),
            "list_count": self.get_listed_count(),
            "average_price": round(self.get_average_listing_price(), 2),
            "median_price": round(self.get_median_listing_price(), 2),
            "max_price": round(self.get_max_listing_price(), 2),
            "daily_volume": round(self.get_daily_volume(), 2),
            "total_volume": round(self.get_total_volume(), 2),
        }
        return output
