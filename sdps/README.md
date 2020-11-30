# Anatomy of SDP

Optional values are specified with `=*` and each field must appear in the 
order shown below.

## Session description
    
`v=`  (protocol version number, currently only 0)\
`o=`  (originator and session identifier : username, id, version number, network address)\
`s=`  (session name : mandatory with at least one UTF-8-encoded character)\
`i=*` (session title or short information)\
`u=*` (URI of description)\
`e=*` (zero or more email address with optional name of contacts)\
`p=*` (zero or more phone number with optional name of contacts)\
`c=*` (connection information—not required if included in all media)\
`b=*` (zero or more bandwidth information lines)\
One or more Time descriptions ("t=" and "r=" lines; see below)\
`z=*` (time zone adjustments)\
`k=*` (encryption key)\
`a=*` (zero or more session attribute lines)\
Zero or more Media descriptions (each one starting by an "m=" line; see below)

## Time description (mandatory)
    
`t=`  (time the session is active)\
`r=*` (zero or more repeat times)\

## Media description (optional)

`m=`  (media name and transport address)\
`i=*` (media title or information field)\
`c=*` (connection information — optional if included at session level)\
`b=*` (zero or more bandwidth information lines)\
`k=*` (encryption key)\
`a=*` (zero or more media attribute lines — overriding the Session attribute lines)\

## Sources

- [SDP](https://en.wikipedia.org/wiki/Session_Description_Protocol)