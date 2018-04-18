#!/usr/bin/env sh

set -e

echo "Welcome to quick & dirty MongoDB cluster generator! Your args are $@"
echo '================================================================================'
./mongodCodeGen.py "$@" | tee mongo_bootstrap_script.sh
echo '================================================================================'
sh mongo_bootstrap_script.sh
echo '================================================================================'
echo 'startup succeed! now you can access from port 27017 to 27017+#routerSize'

# sleep forever
tail -f /dev/null

