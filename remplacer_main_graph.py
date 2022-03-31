import sys
import os, sys
from botorderclient import BotOrderClient
import time
import plotly.express as px
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), 'MSPR_bot_trade'))

from MSPR_bot_trade.selecaoBot import selecaoBot

client = BotOrderClient()
gains = []
timestamp = []
robot = selecaoBot(client)

with open("candle_sample.txt", "r") as fp:
    lines = fp.readlines()
    for line in lines:
        client.process_candle(line)
        robot.process_candle(line)
        gains += [ client.gains() ]
        timestamp += [client.last_time]

print(f"Gains : {client.gains()}")
print(robot.track_gain[-1])
print(len(robot.track_gain))

df = pd.DataFrame(dict(
    x = range(1, len(robot.track_gain)+1),
    y = robot.track_gain
))
fig = px.line(df, x="x", y="y", title="selecaoBot Trade", labels={"x":"Nombre de trades", "y":"Gains"})
fig.show()