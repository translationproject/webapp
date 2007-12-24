#!/bin/bash

# Script that sends the given file to the TP robot.

USERLANG=""    # Default language code, when absent in filename.
STAMP="false"    # Whether to adapt the PO-Revision-Date field.

[ -n "$USERLANG" ] || { echo "Edit script first and set USERLANG."; exit 1; }

[ "$1" == "-n" -o "$1" == "--now" ] && { STAMP="true"; shift; }

file="$1"

[ -n "$file" ] || { echo "Usage:  $0 POFILE
POFILE can be <package_name>-<version>.<lang>.po
           or <package_name>-<version>.po\
"; exit 1; }

[ -f "$file" ] || { echo "No such file: $file"; exit 1; }

[ "${file##*\.}" == "po" ] || { echo "Argument is not a *.po file."; exit 1; }

msgfmt --check $file || { echo "Fix errors first."; exit 1; }

name=${file##*/}
base=${name%\.po}
bare=${base%\.[[:alpha:]_]*}
lang=${base##*\.}

# Fill in the default language code when filename does not contain it.
[ "$bare" == "$base" ] && { lang=$USERLANG; name=$bare.$lang.po; }

# Compare Project-Id-Version with filename.
project=$(sed -n -e '/^\"Project-Id-Version:/{
s/.*: *\([Gg][Nn][Uu] \)*\(.*\)\\n\"/\2/
s/ /-/g
p;q;}' $file)
[ "$name" == "$project.$lang.po" ] || {
    echo "Project-Id-Version '${project/-/ }' does not match filename."
    exit 1;
}

[ "$STAMP" == "true" ] && {
    # Set the revision date to this very moment.
    NEWFIELD="PO-Revision-Date: $(date +"%F %R%z")";
    sed -i "s/^\"PO-Revision-Date:.*\"$/\"$NEWFIELD\\\n\"/" $file;
}

# Send compressed PO file to TP robot.
gzip <$file | uuencode $name.gz |
    mail -s "TP-robot $name" robot@translationproject.org

