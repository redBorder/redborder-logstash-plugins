#!/usr/bin/env bash

# Default values
REMOTE_HOST=""

usage() {
  echo "Usage: $0 -h remote_host"
  echo
  echo "  -h  Remote host (required)"
  exit 1
}

# Parse options
while getopts "h:" opt; do
  case "$opt" in
    h) REMOTE_HOST="$OPTARG" ;;
    *) usage ;;
  esac
done

# Check required argument
if [ -z "$REMOTE_HOST" ]; then
  usage
fi

# Username is always root
USER_NAME="root"

# Base directory is current repo
BASE_DIR=$(pwd)

# Fixed remote cache path
REMOTE_CACHE="/usr/share/logstash/vendor/bundle/jruby/2.5.0/cache/"

echo "Uploading latest .gem files from local subdirectories to $REMOTE_HOST:$REMOTE_CACHE ..."

# Iterate over all local subdirectories
for local_dir in "$BASE_DIR"/logstash-filter-*; do
  [ -d "$local_dir" ] || continue

  # Find the latest .gem in the subdirectory
  latest_gem=$(ls -t "$local_dir"/*.gem 2>/dev/null | head -1)

  if [ -n "$latest_gem" ]; then
    gem_name=$(basename "$latest_gem")
    echo "Uploading $latest_gem to $REMOTE_HOST:$REMOTE_CACHE/$gem_name"

    # Ensure remote cache directory exists
    ssh "$USER_NAME@$REMOTE_HOST" "mkdir -p '$REMOTE_CACHE'"

    # Copy the gem to the remote cache
    scp "$latest_gem" "$USER_NAME@$REMOTE_HOST:$REMOTE_CACHE"
  else
    echo "No gem found in $local_dir"
  fi
done

echo "Upload complete!"
