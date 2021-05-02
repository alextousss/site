inotifywait -e close_write,moved_to,create -m . posts css |
while read -r directory events filename; do
    python build.py
done

