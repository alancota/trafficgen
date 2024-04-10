#!/usr/bin/env python3

import asyncio
import ssl
import sys
from datetime import datetime

import aiohttp

# Disable SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def fetch(session, url, request_number):
    await asyncio.sleep(1)
    print(f"Request [{request_number} of {requests}] - Fetching...")
    start_time = datetime.now()
    async with session.get(url) as response:
        end_time = datetime.now()
        return request_number, response.status, start_time, end_time


async def main(url, requests):
    # Pass the SSL context to the ClientSession
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        tasks = [fetch(session, url, i + 1) for i in range(requests)]
        responses = await asyncio.gather(*tasks)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <URL> <Number of Requests>")
        sys.exit(1)

    url = sys.argv[1]
    requests = int(sys.argv[2])

    asyncio.run(main(url, requests))
