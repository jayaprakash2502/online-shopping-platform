#!/usr/bin/env bash
gunicorn products.wsgi:application