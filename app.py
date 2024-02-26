from flask import Flask, request, jsonify

app = Flask(__name__)

class TietovisaPeli:
    def __init__(self):
        self.kysymykset = ["Mikä on Suomen pääkaupunki?", "Mikä on 16:n neliöjuuri?", "Mikä on maailman suurin valtameri?", "Kuka kirjoitti Romeo ja Julia?", "Mikä on Euroopan korkein vuori?"]
        self.vastaukset = ["Helsinki", "4", "Tyynimeri", "William Shakespeare", "Mont Blanc"]
        self.nykyinen_kysymys_indeksi = 0
        self.pisteet = 0

    def hae_kysymys(self):
        return self.kysymykset[self.nykyinen_kysymys_indeksi]

    def hae_pisteet(self):
        return self.pisteet

    def tarkista_vastaus(self, vastaus):
        oikein = self.vastaukset[self.nykyinen_kysymys_indeksi] == vastaus
        if oikein:
            self.pisteet += 1
        self.nykyinen_kysymys_indeksi = (self.nykyinen_kysymys_indeksi + 1) % len(self.kysymykset)
        return oikein

peli = TietovisaPeli()

@app.route("/")
def info():
    return "Tervetuloa Tietovisa-peliin! Käytä /kysymys saadaksesi kysymyksen ja /vastaus vastataksesi siihen."

@app.route("/kysymys")
def kysymys():
    return jsonify(kysymys=peli.hae_kysymys())

@app.route("/pisteet")
def pisteet():
    return jsonify(pisteet=peli.hae_pisteet())

@app.route("/vastaus", methods=["POST"])
def vastaus():
    data = request.get_json()
    if peli.tarkista_vastaus(data["vastaus"]):
        return jsonify(oikein=True, pisteet=peli.hae_pisteet())
    else:
        return jsonify(oikein=False, pisteet=peli.hae_pisteet())

if __name__ == "__main__":
    app.run(debug=True)