import requests
from itertools import compress
import discord
import me_api

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


def main(request):
    request_json = request.get_json()
    plot_listings(
        request_json["symbol"]
    )  ## /tmp/output/{symbol}_purchase_activities.png
    file = discord.File(
        f"/tmp/{request_json['symbol']}_purchase_activities.png", filename="image.png"
    )
    url = request_json[
        "webhook_url"
    ]  # webhook url, from here: https://i.imgur.com/aT3AThK.png
    output = me_api.floorcheckr.Collections(request_json["symbol"]).listing_data()
    webhook = discord.Webhook.from_url(url, adapter=discord.RequestsWebhookAdapter())
    content = discord.Embed(title=output["symbol"], color=15418782)
    content.set_author(
        name="FloorCheckr",
        icon_url="https://www.freepnglogos.com/uploads/f-logo-orange-png-19.png",
    )
    content.add_field(name="Floor Price", value=output["floor_price"])
    content.add_field(name="# Listed", value=output["list_count"], inline=True)
    content.add_field(name="Average Price", value=output["average_price"], inline=False)
    content.add_field(name="Median Price", value=output["median_price"], inline=False)
    content.add_field(name="Max Price", value=output["max_price"], inline=False)
    content.add_field(name="24 Hour Volume", value=output["daily_volume"], inline=True)
    content.add_field(name="Total Volume", value=output["total_volume"], inline=True)
    content.set_image(url="attachment://image.png")
    content.set_footer(
        text="• Powered by ME •",
        icon_url="https://www.freepnglogos.com/uploads/f-logo-orange-png-19.png",
    )
    webhook.send(file=file, embed=content)
    # https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd
    return {"ok": 200}


def plot_listings(symbol: str):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    sns.set(style="darkgrid")
    listings = me_api.floorcheckr.Collections(symbol).get_price_distribution()
    floor_price = me_api.floorcheckr.Collections(symbol).get_floor_price()
    pretty_symbol = me_api.utils.Utils.prettify_symbol(symbol)
    output_df = pd.DataFrame(listings.items(), columns=["price", "count"])
    sns.set(rc={"axes.grid": True, "savefig.transparent": True})
    ax = sns.displot(
        output_df, x="price", kind="hist", height=6, aspect=2, bins=50, multiple="dodge"
    )
    sns.axes_style(
        style={
            "axes.labelcolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
        }
    )
    plt.axvline(floor_price, color="red", linestyle="--")
    plt.title(
        f"{pretty_symbol} Listings Distribution",
        color="white",
        fontdict={"fontsize": 30},
    )
    plt.xlabel("Price (SOL)", color="white", fontsize=20)
    plt.ylabel("Activity Count", color="white", fontsize=20)
    plt.xticks(color="white", fontsize=20)
    plt.yticks(color="white", fontsize=20)
    plt.savefig(
        f"/tmp/{symbol}_purchase_activities.png", bbox_inches="tight", transparent=True
    )
