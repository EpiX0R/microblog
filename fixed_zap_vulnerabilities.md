## Cookie No HttpOnly Flag [10010]

* Lade till `SESSION_COOKIE_HTTPONLY = True` i app/config.py under Config().
* Lade till `proxy_cookie_path / "/; HTTPOnly; Secure";` i nginx/loadBalancer.cong


## X-Frame-Options Header Not Set [10020]

* Lade till `add_header X-Frame-Options "SAMEORIGIN";` i nginx/loadBalancer.conf


## X-Content-Type-Options Header Missing [10021]

* Lade till `add_header X-Content-Type-Options "nosniff";` i nginx/loadBalancer.conf


## Server Leaks Version Information via "Server" HTTP Response Header Field [10036]

* Lade till `server_tokens off;` i nginx/loadBalancer.conf


## Cookie Without SameSite Attribute [10054]

* Lade till `SESSION_COOKIE_SAMESITE = 'Lax'` i app/config.py under ProdConfig().
* Lade till `proxy_cookie_path / "/; HTTPOnly; Secure";` i nginx/loadBalancer.cong