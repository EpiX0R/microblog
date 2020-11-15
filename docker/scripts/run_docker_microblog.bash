sudo docker run --name microblog -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key \
    --link mysql:dbserver \
    -e DATABASE_URL=mysql+pymysql://microblog:testPW8888@dbserver/microblog \
    microblog:latest