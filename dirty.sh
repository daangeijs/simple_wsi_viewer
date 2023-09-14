#!/bin/bash

# Run the IIPImage server and ensure it stays in the foreground
/usr/lib/iipimage-server/iipsrv.fcgi
tail -f /dev/null
