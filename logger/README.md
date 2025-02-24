# logger 

Cette application python tourne sur Raspberry PI pour l'acquisition des données (logger)
et sur Raspberry ou PC pour l'affichage (monitor). 

Elle permet l'acquisition et l'affichage des températures du chauffage et de la pompe à chaleur 
et d'états électriques (pompes de circulation et boiler) pour la surveillance du chauffage et de l'eau chaude. 

La mesure de température est basée sur des capteurs ds 18b20 et la mesure d'états sur des capteurs 
ds2413 avec une électronique dédicacée.

#### Applications:
- **_logger_** : acquisition des données est activée par crontab toutes les minutes 24/24 365/365
- **_monitor_** : permet l'analyse et l'affichage graphiques des mesures
