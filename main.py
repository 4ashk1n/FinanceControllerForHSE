from config import *
from web import *
from engine import *

"""
// Copyright © 2022 Schagin Dmitry. All rights reserved.
"""

db_import()

# print(str(ssh_tunnel.public_url) + '/operations')
# print(str(ssh_tunnel.public_url) + '/login')
# print(str(ssh_tunnel.public_url) + '/reg')
# print(str(ssh_tunnel.public_url) + '/stats')
# print(str(ssh_tunnel.public_url) + '/categories')
# print("http://localhost:302" + '/profile')


app.secret_key = 'YourSecretKey'
# for k in range(32):
#     app.secret_key += "DNCFTB"[random.randint(0,5)]

if __name__ == '__main__':
    app.run()

