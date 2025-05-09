# Cloudflare Bypass

A Python tool to bypass Cloudflare bot protection by automating browser verification and transferring the resulting cookies into a `requests.Session` for seamless HTTP requests.

## Features

- Utilizes [DrissionPage](https://github.com/g1879/DrissionPage) for Chromium-based browser automation.
- Automatically locates and interacts with Cloudflare Turnstile verification buttons.
- Extracts valid cookies and injects them into a `requests.Session`.
- Simple API for easy integration into your Python scripts.

## Example Usage
```py
from app import cf_bypass
import requests

url = "https://example.com/"


bypasser = cf_bypass()
session = requests.Session()
bypasser.bypass_cloudflare(url, session)

# now we have safe session for bypassing cloudflare bot protection
response = session.get(url)
print(response.text)


```
