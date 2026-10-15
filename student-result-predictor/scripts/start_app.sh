#!/bin/bash
set -e
systemctl daemon-reload
systemctl enable student-app
systemctl restart student-app
sleep 2
systemctl is-active --quiet student-app
