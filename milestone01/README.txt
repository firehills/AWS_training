# Running the example

## Users

Need to create a pool of users for our app

### Web Portal 
Cognito->Create user pool
on left "Users" then "Create User"

(Note email should be unique for that user pool)



### Change password via cmd line

```bash
aws cognito-idp admin-set-user-password \
  --user-pool-id us-east-1_eJg72xFLu \
  --username whatever@gmail.com \
  --password Password123! \
  --permanent
```


## Frontend

Running the frontend 

```sh
cd milestone01\frontend
npm install
npm run dev
```

