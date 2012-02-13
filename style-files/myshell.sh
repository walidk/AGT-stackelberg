#!/bin/bash
CONF_FILE=$(grep IEEEconf ~/Library/Application\ Support/LyX-2.0/clsFiles.lst -m 1)
mv $CONF_FILE $CONF_FILE".old"
wget "http://css.paperplaza.net/conferences/support/files/ieeeconf.cls" -O $CONF_FILE
echo "now go to lyx, and click Lyx->Reconfigure, then restart. Then change class to article (IEEEconf)"