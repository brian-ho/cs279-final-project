# Can You Find Me Now?
# Utilizing Crowdsourcing to Conduct Geolocation with Noisy Information
**CS279 Final Project**

## Abstract
The precise reporting of an object's location in physical space to facilitate finding of that object in the real-world is an essential task in a number of geospatial domains and activities. While existing solutions rely on real-time conversation in the context of a rendezvous with a knowledgeable partner or supply descriptive visuals, few options provide precise locations at scale, in the field, and with minimal original inputs (limited to a GPS location and text description). Our approach leverages crowdsourcing to provide close-in location information in a manner that could accommodate motivated volunteers or communities on-site; we utilize an opt-in controlled experiment with participants on Amazon MechanicalTurk and Google StreetView imagery to study this approach. We find [TODO: RESULTS]. The primary contribution is a crowd-powered system that iteratively improves location descriptions. Additionally, based on the updated descriptions in each cycle and task completion time data, we are able to learn characteristics of good descriptions. Finally, we contribute the interface design of the crowd-powered system. This includes the layout of the web page and overall interaction model.

## Usage
Run `MT_scripts/post_hits.py task-type trial-number` to intialize HITs on Amazon MechanicalTurk

## Credits
Arman Hassan, Brian Ho, Vish Srivatsa
