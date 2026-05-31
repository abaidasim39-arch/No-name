import time
import requests

def check_network_forever():
    url = "https://speedtest.net"
    
    # Try block taaki agar android module na mile to Windows par crash na ho
    try:
        from android import api_version
        print(f"ASIM Service: Level {api_version} par chal rahi hai")
    except ImportError:
        print("ASIM Service: Testing mode")

    while True:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"ASIM Service: ✅ Connected ({response.status_code})")
            else:
                print(f"ASIM Service: ⚠️ Code {response.status_code}")
        except Exception as e:
            print(f"ASIM Service: ❌ Error ({str(e)[:30]})")
            
        # Har 5 seconds baad internet check karega
        time.sleep(5)

if __name__ == '__main__':
    check_network_forever()
