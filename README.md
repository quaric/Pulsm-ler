Dette er en ROS-applikasjon som benytter en BeagleBone Black med en fotoplesmytograf for å lese av puls. 
Prosjektet er skrevet i Python, og starter en matplot graf, samt printer ut pulsen i en konsoll. 


Komponenter

fotoplesmytograf.py:
Dette er en publisher node som publiserer sensorverdier fra sensorene. Den kobler seg på topic
«fpmg_raw», og publiserer en message som kalles «raw_sensor_value». Denne messagen inneholder
3 floats: timeinmillis, voltage og temperatur. Egentlig så kunne den bare inneholdt voltage, men jeg
var litt usikker på hva dere forventet så jeg bare inkluderte alt.
Som i forrige oblig så sjekker programmet temperaturen i en egen tråd, og temperatur variablen
oppdateres ca. hvert 800ms. Spenningsverdien i TRCT1000-sensoren sjekkes 7 ganger i sekundet, like
ofte som noden publiserer på topicen.

lpfilter.py:
Dette er en hybrid-node. På «fpmg_raw» topicen er den en Subscriber, mens den er en client til
do_filter_calc-service noden, og samtidig en publisher-node på «fpmg_filtered».
Når den mottar nye verdier på «fpmg_raw» så kaller den metoden «filter_values», denne callbackmetoden sender «raw_sensor_value.msg» messagen den mottar til do_filter_calc-servicenoden.
Mellom lpfilter.py og do_filter_calc.py kommuniseres det med srv-typen «filtered_sensor_value.srv».
Som request så sender den 3 float verdier: timeinmillis, voltage og temperatur. Som response sender
den tilbake to float verdier: sum og raw. Sum representerer den filtrerte verdien, mens raw er
voltage verdien som ble sendt inn til filtrering.
Når lpfilter mottar filtered_sensor_valueResponse fra do_filter_calc, så kalles metoden
«handle_filtered_value» som blir lagt i en «filtered_value» - message og publisert på
«/fpmg_filtered»

do_filter_calc.py:
do_filter_calc.py er en service-node. Den mottar en filtered_sensor_valueRequest og voltage verdien
på slutten av en queue. Den regner så ut den nye filter verdien, som legges på slutten av en queue
som tar vare på tidligere filterverdier.
Filter verdien regnes ut slik: y = -a1*y1 - a2*y2 + b1*u1 + b2*u2
Hvor u1 og u2 er tidligere råverdier fra voltage som har blitt lagret i en queue med størrelse på 3.
Y1 og y2 er tidligere filterverdier som har blitt lagret i en annen queue med størrelse på 3.
A og b er konstanter som ble regnet ut i matlab.
Så returneres den nye filterverdien(y) sammen med den rå voltage-verdien som en
filter_sensor_valueResponse, begge som float.evaluate_data.py:
Dette er en Subscriber-node, den subscriber på topicen «/fpmg_filtered». Når den får en ny verdi så
vil den kalle på metoden «print_values». Denne metoden printer ut den rå og filtrerte verdien.
I tillegg så forsøker den også å regne ut puls. Det gjør den ved å:
Holde på tid: +142.85714 ved hver oppdatering, siden vi skal ha en oppdateringsfrekvens på 7hz
Holde på 5 siste verdier i en queue/liste.
Finne den høyeste verdien i listen og lagre den i highestvalue, så sammenligne denne verdien med ny
data, og inkrementere count med +1, dersom vi har en ny highestvalue.
Tanken er da at vi teller antall lokale topper i grafen, og dette er det count representerer.
Vi regner så ut pulsen fra dataen vi har slik:
Puls = (count/(timeinmillis/1000))*60
