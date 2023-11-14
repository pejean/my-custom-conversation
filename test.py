import aiohttp
import asyncio

async def send_message_to_api_async(message):
    url = 'http://127.0.0.1:8555'
    payload = {'message': message}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    response_data = await response.json()
                    result = response_data['message']
                else:
                    result = f"Communication Error: {response.status}"
    except aiohttp.ClientError as e:
        result = f"HTTP client error: {e}"
    except asyncio.TimeoutError:
        result = "Request timed out"
    except Exception as e:
        result = f"An unexpected error occurred: {e}"

    return result

async def main():
    result = await send_message_to_api_async("Bonjour, ceci est un test.")
    print(result)

asyncio.run(main())