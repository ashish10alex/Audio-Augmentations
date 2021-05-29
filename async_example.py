import asyncio
import time

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

async def async_get_data():
    await asyncio.sleep(2)
    print('Asnc function called')
    return ' done!'

def sync_get_data():
    time.sleep(2)
    print('Sync function called')
    return ' done!'

@app.route("/sync")
def sync_req():
    start = time.time()
    sync_get_data(),
    sync_get_data(),
    sync_get_data()
    total_time =  time.time() - start
    return f'<h2> Finally done {total_time :.5f} secs </h2>'



@app.route("/async")
async def async_req():
    start = time.time()
    data = await asyncio.gather(
            async_get_data(),
            async_get_data(),
            async_get_data()
            ) 
    total_time =  time.time() - start
    return f'<h2> Finally done {total_time :.5f} secs </h2>'

if __name__ == '__main__':
    app.run(debug=True, port=3000)

