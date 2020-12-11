
# Redis

The Redis keyspace notifications can be used as a mean to synchronize session 
information among different rtpengine instances. This is especially useful if 
one needs to realize a redundant media relay setup. In such a setup, rtpengine 
machines can be configured to act, at the same time, both as:

- **active** machine 
  - create calls via offer()/answer(), counted as OWN calls.
  - destroy calls 
- **passive** (backup) machine
  - create new calls via SADD notifications, counted as FOREIGN calls.
  - destroy calls 

rtpengine will always differentiate between:

- **OWN** calls: 
  - created via offer()/answer()
  - destroyed, by delete() 
- **FOREIGN** calls: 
  - created via SADD notification
  - destroyed DEL, FINAL_TIMEOUT or cli