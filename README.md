# Setup

```bash
python3 -m venv venv
source venv/bin/activate #(geht auf Windows vermutlich anders)
pip install -r requirements.txt
```

## Datenq
Die Datenquellen sind

### sales
https://www.kaggle.com/datasets/leonczarlinski/iowa-liquor-sales

### population
https://www.kaggle.com/datasets/zusmani/us-census-2020?select=Iowa_IA.csv

## csvs entpacken

die beiden gezippten CSV Dateien entpacken

# run

```bash
source venv/bin/activate #(geht auf Windows vermutlich anders)
python3 main.py
```

Das Programm lädt standardmäßig die kleine Datei, die 1/100 der Daten enthält, um die Entwicklung schneller zu gestalten.

Für die volle Analyse einfach 

````python
data = pd.read_csv("sales_sampled.csv")
````
durch
````python
data = pd.read_csv("sales.csv")
````
ersetzen