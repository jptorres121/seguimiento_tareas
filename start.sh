#!/bin/bash

# Migración e inicio
uvicorn app.main:app --host 0.0.0.0 --port 10000
