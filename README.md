# GPS-reporter is written in the python language.
It reads a xml-file from GPS loggers and makes a report with date; start-address(or zip-code); travelled-distance; end-address(or zip-code).
Searches for the zip-code based on geocoders Nominatim for a start address.
It keeps a record of the distance and time traveled.
If there is no movement for more then 5 minutes then it starts a new line.
