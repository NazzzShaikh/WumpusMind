import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import json

def run_test():
    print("Testing /api/setup...")
    req = urllib.request.Request('http://localhost:5000/api/setup', 
        data=json.dumps({"size":4, "difficulty":"Easy", "algorithm":"Hybrid", "play_mode":"autoplay"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    resp = opener.open(req)
    print(resp.read().decode())
    
    print("Testing /api/step loop...")
    for i in range(10):
        try:
            req_step = urllib.request.Request('http://localhost:5000/api/step', method='POST')
            resp_step = opener.open(req_step)
            data = json.loads(resp_step.read().decode())
            print(f"Step {i}: status={data.get('status')}")
            if data.get('decision'):
                print(f"   Reason: {data['decision'].get('reason')}")
            if data.get('status') == 'game_over' or (data.get('decision') and ('DEATH' in data['decision'].get('reason', '') or 'VICTORY' in data['decision'].get('reason', ''))):
                print("Game over detected.")
                break
        except Exception as e:
            print(f"Error on step {i}: {e}")
            break
            
if __name__ == '__main__':
    run_test()
