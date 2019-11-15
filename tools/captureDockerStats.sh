#!/bin/bash
while true; do docker stats --no-stream | tee -a stats.txt; sleep 0.5; done