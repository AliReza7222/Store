# Store
This project is a bookstore for buying and selling books. You can share your books for sale or you can top up your account and buy books. This project is created from four programs and I will explain each one to you below. The database project is configured on postgresql and I use environs to configure my settings and you have to do the settings.

### App accounts :
This app created for authentication and model User and Profile and login and logout .

### App Books :
This app is for any book view and created model Book and model Review .

### App Cart:
This app is created for your shopping cart and the books you choose to buy are implemented using this app.

### App Pages :
This app is for views Home and About and PaymentSimulator and other view site .

### Run Project :
  1. you first must install packages from `requirements.txt`.
      ```
        pip install -r requirements.txt
      ```
2. You need to configure the project ***settings*** and you must put a ***valid email*** in.  
     - `   EMAIL_HOST = env('EMAIL_HOST') `
     - `   EMAIL_HOST_USER = env('EMAIL_HOST_USER') `
     - `   EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD') `
  
