# TE-ilmoitukset
### Ohjelman kuvaus:
Ohjelma hakee te-palvelut.fi sivulta RSS-syötteenä uusimmat työpaikkailmoitukset ja listaa ne exceliin.

### Esimerkkikäyttö oletusarvoilla:

Aineiston voi noutaa kertaluonteisesti komennolla 
```python 
python te_palvelut.py
```

tai automaattisesti noin 25 min (1500 sec) välein komennolla 
```python
python run_loop.py
```

### Lisätietoja ohjelmasta:
Ohjelma on tarkoitettu helpottamaan te-palvelut.fi sivun
työilmoitusten läpikäyntiä. Te-palveluiden työnhakusivulta
ei saa listattua ilmoituksia uusimmasta vanhimpaan, vaan 
ainoastaan epäkronologisesti 24h, 3 päivää, viikko tai kaksi
viikkoa mukaan, joten usein joutuu selaamaan samoja 
ilmoituksia monta kertaa. Lisäksi ilmoituksia voi rajata 
pois vain ammattiryhmittäin ja usein ilmoitukset saattavat 
olla väärässä luokassa. Tätä varten ohjelmalla voi 
hakusanoilla rajata pois ilmoituksia. 

Hakusivulta saa muodostettua RSS/XML-tiedoston, jossa näkyy 
200 uusinta ilmoitusta item-elementtien muodossa. Tämä 
aiheuttaa sen, että ohjelma on ajettava melko usein 
hakuehdoista riippuen (haulla Helsinki, Vantaa ohjelma pitää 
ajaa noin 4 kertaa päivässä). Tätä varten ohjelma sisältää 
aikakatkaisulla toimivan pääohjelman (run_loop.py), joka ajaa 
varsinaisen koodin (te_palvelut.py).

### Lisätietoja käytöstä:
* Tee [te-palvelut.fi](https://paikat.te-palvelut.fi/tpt/) sivulla työpaikkailmoitushaku valinnaisilla spekseillä ja muodosta oikeassa kulmassa olevasta RSS- painikkeesta XML-tiedosto. Kopioi url ja liitä te_palvelut.py tiedoston main()-funktioon url-muuttujaan.

* Määritä del_titles.txt -tiedostoon allekkain hakusanat, joita et halua sisältyvän ilmoitusten otsikoissa.

* lokitiedot ajosta löytyy tiedostosta example.log
  * ”kaatui”: ajo ei onnistunut, eikä tietoja siirretty exceliin, yritä uudelleen
  * ”Dataa haettu liian harvoin”: edellisestä tietojen hausta on liian kauan/ ilmestyy automaattisesti ensimmäisen ajon aikana
    * Jos tämä ilmestyy toistuvasti, niin muokkaa run_loop.py -tiedoston SEC-muuttujaan pienempi luku
* te_palvelut.py tiedostosta löytyy metodi clear_excel() excelin tyhjentämiseksi, mutta se ei oletusarvoisesti ole käytössä.
