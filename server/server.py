from flask import Flask, jsonify

app = Flask(__name__)

# アップデート情報のダミーデータ
# 実際のアプリでは、この情報をデータベースなどから取得します
UPDATE_INFO = {
    "version": "1.1.0",
    "has_update": True,
    "download_url": "https://example.com/GeneralManagementTool-1.1.0.exe"
}

@app.route('/check_for_updates')
def check_for_updates():
    return jsonify(UPDATE_INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)