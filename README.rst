==========
VMAP Knife
==========

Takes a CSV export of a Charles session and VMAP document and produces a report showing
which ad breaks triggered which external calls. The project is designed to reduce the 
amount of time required to validate VMAP / VAST player behaviour. 

Usage
-----

Requires:
 - Python 3.8
 - pip3

Steps:
 - Install pip3 
 - Run `pip3 install virtualenv`
 - Run `virtualenv venv`
 - Run `. venv/bin/activate`
 - Run `pip3 install --editable .`
 - Run `vmap_knife --csvfile input.csv --vmapfile input.xml --outputfile report.html`


 Developer Notes
 ---------------

 