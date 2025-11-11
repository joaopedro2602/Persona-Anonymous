#!/bin/bash
export $(grep -v '^#' .env | xargs)
python app/app.py