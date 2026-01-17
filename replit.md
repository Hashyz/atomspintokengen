# AtomSpinZone Token Fetcher

## Overview
A mobile-friendly Python script for Termux that fetches access tokens from AtomSpinZone.

## How to Use on Termux

### Installation
```bash
pkg update && pkg upgrade
pkg install python
pip install requests
```

### Download and Run
```bash
python main.py
```

## How It Works
1. Requests initial URL to get MSISDN from redirect
2. Follows the redirect to activate session
3. Calls API to fetch access token
4. Displays token, phone number, and spins

## Requirements
- Mobile data connection (required for carrier detection)
- Python 3.x
- requests library

## Output
- Token (JWT)
- Phone number
- Available spins
- Account name

## Recent Changes
- 2026-01-17: Initial creation of mobile-friendly script
