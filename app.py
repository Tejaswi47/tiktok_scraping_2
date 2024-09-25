from tiktok_scraping import Connection
import time
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/vpn_connection', methods = ['GET'])
def start_vpn_connection():
    global chrome_browser
    chrome_browser = Connection()
    time.sleep(15)
    chrome_browser.sign_to_proton()
    time.sleep(15)
    chrome_browser.sign_to_vpn()
    time.sleep(15)
    chrome_browser.switch_vpn()
    time.sleep(15)
    chrome_browser.connect_vpn()
    return jsonify({'message': "vpn established"})

@app.route('/search_user/<path:username>', methods=['GET'])
def search_user(username):
    try:
        chrome_browser.search_tiktok_user(username)
        time.sleep(15)
        users_data = chrome_browser.extract_users()
        final_data = []
        for i in users_data:
            result = []  
            lines = i.split('\n')  
            for line in lines:
                result.extend(line.split(' · '))  
            temp_dict = {
                'username': result[0] if len(result) > 0 else None,
                'Nickname': result[1] if len(result) > 1 else None,
                'followers': result[2] if len(result) > 2 else None,
                'bio': result[3] if len(result) > 3 else None
            }
            
            final_data.append(temp_dict) 
        return jsonify({'sucess': True, 'data': final_data, 'message': "Completed successfully"})
    except Exception as e:
        return jsonify({'sucess': False, 'data': '', 'message': str(e)}) 
# {'username': username,'nickname}

if __name__ == '__main__':
    app.run(debug=False)
    
    




