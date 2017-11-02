# Installing and running for the first time
1. Prepare the `config.cfg` based on the provided template file: `cp config-template.cfg config.cfg`
2. Open the newly created config.cfg file with your favourite Terminal-based text editor: `nano config.cfg`
3. Fill in all the config value.
4. Install the app: `bash install.sh`
6. Run the app: `bash run.sh`

# Running in debug mode
`bash run-debug.sh`

# API
**Municipality Procurement API**
This is the API of [e-prokurimi](e-prokurimi.org) platform that visualizes procurement data from local municipality and automatically detects irregularities through a contextual and custom built red flagging algorithm.
* **URL**
[http://e-prokurimi.org/api/municipality-procurements/](http://e-prokurimi.org/api/municipality-procurements/)

* **Allowed HTTPs requests**
  `GET`

* **JSON structure**
Sample JSON body structure
```
{
	"_id" : ObjectId("59f6e4a6e4f9620441c65915"),
	"viti" : 2012,
	"tipiBugjetit" : "Të hyra vetanake",
	"klasifikimiFPP" : 30,
	"tipi" : "Shërbime",
	"kontrata" : {
		"qmimi" : 500,
		"vlera" : 500,
		"afatiKohor" : "Afati kohor normal",
		"kriteret" : "Çmimi më i ulët",
		"qmimiAneks" : 0
	},
	"kompania" : {
		"tipi" : "OE Vendor",
		"emri" : "Lorem Ipsum",
		"slug" : "lorem-ipsum",
		"selia" : {
			"emri" : "Prishtina",
			"kordinatat" : {
				"gjeresi" : 42.6662068,
				"gjatesi" : 21.1599254
			},
			"slug" : "prishtine"
		}
	},
	"numri" : 1,
	"dataNenshkrimit" : ISODate("2012-01-27T00:00:00Z"),
	"komuna" : {
		"emri" : "Prishtina",
		"slug" : "Prishtina"
	},
	"vlera" : "Vlerë e vogël",
	"procedura" : "Procedura e kuotimit të Çmimeve",
	"aktiviteti" : "Transmetimin integral të seancave të Kuvendit."
}
```
* **Server Responses**
⋅⋅* 200 `OK` - the request was successful
⋅⋅* 204 `No Content` - the request was successful but there is no representation to return (i.e. the response is empty)
⋅⋅* 400 `Bad Request` - the request could not be understood or was missing required parameters.
⋅⋅* 401 `Unauthorized` - authentication failed or user doesn't have permissions for requested operation.
⋅⋅* 403 `Forbidden` - access denied.404 Not Found - resource was not found.

* **All URL Params**
⋅⋅* `string:komuna`   - Municipality.

Possible options:
1. `ferizaj`
2. `gjakova`
3. `gjilan`
4. `prishtina`
5. `vitia`
6. `hani-i-elezit`

⋅⋅* `int:year`

Possible options:
1. `2010`
2. `2011`
3. `2012`
4. `2013`
5. `2014`
6. `2015`
7. `2016`

⋅⋅* `company-slug`
Slang of the company.


## API calls

## GET `/budget-type/<string:komuna>/<int:year>`
* **Required Prams**
..* `string:komuna`
..* `int:year`

Sample Call:  [http://e-prokurimi.org/api/municipality-procurements/budget-type/prishtina/2012](http://e-prokurimi.org/api/municipality-procurements/budget-type/prishtina/2016)


## GET `/procurement-type/<string:komuna>/<int:year>`
* **Required Prams**
..* `string:komuna`
..* `int:year`

Sample Call:  [http://e-prokurimi.org/api/municipality-procurements/procurement-type/prishtina/2012](http://e-prokurimi.org/api/municipality-procurements/procurement-type/prishtina/2012)


## GET `/<string:komuna>/monthly-summary`
* **Required Prams**
..* `string:komuna`

Sample Call:  [http://e-prokurimi.org/api/municipality-procurements/prihstine/monthly-summary](http://e-prokurimi.org/api/municipality-procurements/procurement-type/prishtina/2012)


## GET `/monthly-summary/<int:viti>`
* **Required Prams**
..* `string:viti`

Sample Call: [http://e-prokurimi.org/api/municipality-procurements/monthly-summary/2014](http://e-prokurimi.org/api/municipality-procurements/monthly-summary/2014)

## GET `/kompania/<string:company-slug>`
* **Required Prams**
..* `string:company-name`

Sample Call: [http://e-prokurimi.org/api/municipality-procurements/kompania/abc](http://e-prokurimi.org/api/municipality-procurements/kompania/abc)

## GET `/kompania-detajet/<string:company-slug>`
* **Required Prams**
..* `string:company-slug`

Sample Call: [http://e-prokurimi.org/api/municipality-procurements/kompania-detajet/abc](http://e-prokurimi.org/api/municipality-procurements/kompania-detajet/abc)


## GET `<string:komuna>/red-flags/<int:viti>`
* **Required Prams**
..* `string:komuna`
..* `int:year`

Sample Call: [http://e-prokurimi.org/api/municipality-procurements/prishtina/red-flags/2012](http://e-prokurimi.org/api/municipality-procurements/prishtina/red-flags/2012)

## GET `<string:komuna>/treemap/<int:viti>`
* **Required Prams**
..* `string:komuna`
..* `int:year`

Sample Call: [http://e-prokurimi.org/api/municipality-procurements/prishtina/treemap/2012](http://e-prokurimi.org/api/municipality-procurements/prishtina/treemap/2012)

## GET `<string:komuna>/piechart/<int:viti>`
* **Required Prams**
..* `string:komuna`
..* `int:year`

Sample Call: [http://e-prokurimi.org/api/municipality-procurements/ferizaj/piechart/2012](http://e-prokurimi.org/api/municipality-procurements/ferizaj/piechart/2012)
