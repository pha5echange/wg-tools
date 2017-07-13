# WG-Tools

Tools for processing Wikidata genre data. 

Requires Python 2.7, the 'numpy' library, the 'networkx' library, the 'community' library, and the 'matplotlib' library. 

The file 'rawdata/wiki_genres_data.txt' must be present. 
This contains a list of genres and sub-genre relationships, generated via a query to the Wikidata public query service:
https://query.wikidata.org


SPARQL query example (Music genres)


SELECT ?itemLabel ?item ?_subclass_ofLabel ?influenced_byLabel ?based_onLabel ?inspired_byLabel

WHERE {

  ?item wdt:P31 wd:Q188451.
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language"en,fr,de,nl,it,pt,ast,ca,es,qu,ar,hy,cs,ru,da,fi,vi,ja,zh". }
  
  OPTIONAL { ?item wdt:P279 ?_subclass_of. }
  
  OPTIONAL { ?item wdt:P737 ?influenced_by. }
  
  OPTIONAL { ?item wdt:P144 ?based_on. }
  
  OPTIONAL { ?item wdt:P941 ?inspired_by. }
  
}
