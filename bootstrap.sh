#!/usr/bin/env bash

set -e
set -o pipefail

echo "Welcome to quick & dirty MongoDB cluster generator! Your args are $@"
echo '================================================================================'
./mongodCodeGen.py "$@" | tee mongo_bootstrap_script.sh
echo '================================================================================'
echo 'running...'
sh mongo_bootstrap_script.sh
echo '================================================================================'
echo 'startup succeed! now you can access from port 27017 to 27017+#routerSize'
echo 'for more information, see https://github.com/xplorld/MongoDBClusterOnDocker'

# sleep forever
tail -f /dev/null

