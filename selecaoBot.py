import json 
class selecaoBot():

    def __init__(self,client):
        self.client = client  
        self.total_AAPL = 0
        self.count_AAPL = 0
        self.previous_price = 0
        self.track_gain = []

    def process_candle(self, candle_msg:str):
        """This function is called when a new candle_msg is received.
            Candle message is a string of the form:
            'symbol_key' : {'c': [174.3], 'h': [174.3], 'l': [174.19], 'o': [174.19], 's': 'ok', 't': [1643670000], 'v': [1888]}

            Note that there are list, so you can have multiple candles in one message.
        """
        candle_dict = json.loads(candle_msg)                           #transforme le fichier json en dictionnaire 
        for k, v in candle_dict.items():
            bon_prix = self.client.money * 0.001
            if 'AAPL' == k :
                self.update_aapl_mean(v)
                
                #print(f"Moyenne :{self.total_AAPL/self.count_AAPL}")
                #self.sell_if_needed(k, v)
            self.chute_prix(k, v, bon_prix)
            self.previous_price = v['c']

        def strategie_1 ():
            for k,v in candle_dict.items():
                self.client.buy(k,0.001)
                self.track_gain.append(self.client.gains())
        strategie_1()
        def strategie_3():
            for k,v in candle_dict.items():
                interet = v['v']
                rapport2 = v['h'] + v['l'] / 2
                if interet > 1000 and rapport2 > 20:
                    self.client.buy(k,0.1)
                    self.track_gain.append(self.client.gains())
    def chute_prix(self, k, v, bon_prix):
        """permet d'acheter une action quand son prix chute, et qu'elle avait de la valeur avant. 
        l'action reprendra de la valeur et nos actions avec"""
        prix_interessant = 0                                                 #donner une valeur directement
        if v['c'] < bon_prix and self.previous_price > v['c'] :
            self.client.buy(k,2)
            self.track_gain.append(self.client.gains())


    def update_aapl_mean(self, v):                                       #remanier ctrl shift r, permet de cr??er une m??thode sans la r????crire, plus clair
        self.count_AAPL += 1
        self.total_AAPL += v['c']

                
    def sell_if_needed(self, k, v):
        if v['c'] < self.previous_price  : 
            self.client.sell(k,1)
            self.track_gain.append(self.client.gains())
        elif self.client.money > v['c']: 
            self.client.buy(k,1)
            self.track_gain.append(self.client.gains())
