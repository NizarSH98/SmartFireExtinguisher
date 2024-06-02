#!/bin/bash
sleep 30   # Wait for 30 seconds
# Set the DISPLAY environment variable
export DISPLAY=:0
# Log file path
LOG_FILE="/home/admin/Desktop/run_scripts.log"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Start of script execution
log "Script execution started"

# Run braodcast.py in a new terminal window
xterm -fa 'Monospace' -fs 12 -e python3 /home/admin/Desktop/Broadcast/Broadcast.py >> "$LOG_FILE" 2>&1 &

# Run detect.py in a new terminal window
xterm -fa 'Monospace' -fs 12 -e python3 /home/admin/Desktop/yolov5-fire-detection-main/detect.py >> "$LOG_FILE" 2>&1 &

# End of script execution
log "Script execution finished"
