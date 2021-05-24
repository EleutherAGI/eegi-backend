# eegi-backend

# How to use it:

## JTW Token Authentication

JTW Signing using RSA256

To generate 2048-bit RSA key pair, use the following
```
cd app
openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem
```

## Running backend

To get the backend to run locally cd into the app and run with uvicorn

```
cd app
uvicorn main:app --reload
```