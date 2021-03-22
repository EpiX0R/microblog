#!/bin/bash

# Reads AWS cridentials from clipboard, formats them and inserts to file. Keeping the file encrypted after.
# Should work with WSL or bash environments where xclip is installed.
# Put ansible cridentials in a config file and add to ENV to avoid the need to input password all the time.
# Need dos2unix installed. Might not be needed on a Linux computer.
# Need gsed installed on MacOSX.

sed_type="sed"

if [ -x "$(command -v powershell.exe)" ]; then
    copied_text=$(powershell.exe Get-Clipboard)
elif [[ "$OSTYPE" == "darwin"* ]]; then
    sed_type="gsed"
    copied_text=$(pbpaste)
else
    copied_text=$(xclip -o)
fi

copied_text=$(echo "$copied_text" | dos2unix)

export AWS_ACCESS_KEY="$(echo "$copied_text" | $sed_type -n -E 's/aws_access_key_id=(.+)/\1/p')"
export AWS_ACCESS_KEY_ID="$(echo "$copied_text" | $sed_type -n -E 's/aws_access_key_id=(.+)/\1/p')"
export AWS_SECRET_ACCESS_KEY="$(echo "$copied_text" | $sed_type -n -E 's/aws_secret_access_key=(.+)/\1/p')"
export AWS_SECRET_KEY="$(echo "$copied_text" | $sed_type -n -E 's/aws_secret_access_key=(.+)/\1/p')"
export AWS_SECURITY_TOKEN="$(echo "$copied_text" | $sed_type -n -E 's/aws_session_token=(.+)/\1/p')"
export AWS_SESSION_TOKEN="$(echo "$copied_text" | $sed_type -n -E 's/aws_session_token=(.+)/\1/p')"
