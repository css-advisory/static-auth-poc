# Static File Authorization Examples

This repository contains several different examples of how to control access to staticfiles. All of these examples are built in docker containers for portability.

All applications contained within this repository will look identical. The only differences are in how the static files are protected. 

These examples were discussed during a booth talk at Blackhat USA 2017. The slides from that presentation can be found [here](https://www.slideshare.net/AlecGleason1/static-files-in-the-modern-web-age)

### Not for production use
These proof-of-concept apps do not contain many protections and are intended just to demonstrate various ways of authorizing use of static files.

# PoC Requirements
* `docker`: https://www.docker.com/community-edition 
* `docker-compose`
