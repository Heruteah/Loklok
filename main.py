import requests
import os
import asyncio
import aiohttp
import re
import sys
from rich.console import Console

info = {
    "owner": 'nigga',
    "facebook": 'Jay Mar',
    "tool": 'Spamshare',
    "version": '1',
}

config = {
    'cookies': '',
    'post': ''
}

console = Console()
os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    art = f"""
[bold red]▒█▀▀▀ █▀▀▄ ░░ █▀▀ █░░█ █▀▀█ █▀▀█ █▀▀
▒█▀▀▀ █▀▀▄ ▀▀ ▀▀█ █▀▀█ █▄▄█ █▄▄▀ █▀▀
▒█░░░ ▀▀▀░ ░░ ▀▀▀ ▀░░▀ ▀░░▀ ▀░▀▀ ▀▀▀[/bold red]

[cyan]{'='*60}[/cyan]
[green]TOOL     : {info['tool']}   |   VERSION: {info['version']}[/green]
[yellow]OWNER    : {info['owner']}   |   FACEBOOK: {info['facebook']}[/yellow]
[cyan]{'='*60}[/cyan]
"""
    console.print(art)

banner()
config['cookies'] = input("\033[0mCOOKIE : \033[92m")
config['post'] = input("\033[0mPOST LINK : \033[92m")
share_count = int(input("\033[0mSHARE COUNT : \033[92m"))

if not config['post'].startswith('https://'):
    console.print("[red]Invalid post link[/red]")
    sys.exit()
elif not share_count:
    console.print("[red]No count provided.[/red]")
    sys.exit()

os.system('cls' if os.name == 'nt' else 'clear')
console.print("[yellow][*][/yellow] Checking your inputs, please wait...")

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1'
}

class Share:
    async def get_token(self, session):
        headers['cookie'] = config['cookies']
        async with session.get('https://business.facebook.com/content_management', headers=headers) as response:
            data = await response.text()
            token_match = re.search(r'EAAG(.*?)","', data)
            if not token_match:
                raise Exception("Failed to extract token.")
            return 'EAAG' + token_match.group(1), headers['cookie']

    async def share(self, session, token, cookie):
        headers['accept-encoding'] = 'gzip, deflate'
        headers['host'] = 'b-graph.facebook.com'
        headers['cookie'] = cookie
        count = 1
        os.system('cls' if os.name == 'nt' else 'clear')
        with console.status("[bold green]Sharing Facebook post..."):
            while count <= share_count:
                async with session.post(
                    f'https://b-graph.facebook.com/me/feed?link={config["post"]}&published=0&access_token={token}',
                    headers=headers
                ) as response:
                    try:
                        data = await response.json()
                        if 'id' in data:
                            console.log(f"[green]{count}/{share_count} Complete[/green]")
                            count += 1
                        else:
                            console.log("[red]Cookie may be invalid or blocked.[/red]")
                            break
                    except Exception as e:
                        console.log(f"[red]Failed: {e}[/red]")
                        break
        console.print(f"[bold green][✓][/bold green] Sharing post done!")

async def main():
    async with aiohttp.ClientSession() as session:
        share = Share()
        token, cookie = await share.get_token(session)
        await share.share(session, token, cookie)

asyncio.run(main())
