import botometer
from flask import Flask

rapidapi_key = 'ef553c612emsh0aab3806e0dc54cp1fdb75jsn595045496df5'
twitter_app_auth = {
    'consumer_key': 'rNYaIMBoelVLAJEJIh4DtZaQS',
    'consumer_secret': 'h4zsiN5O1XGzLWokMfphmN2yu3IjHK18LJ6dc7WVLbDnxa4xhY',
    'access_token': '1567967854271827970-i2mvPFTRg8UPqvHzVZYZKZwdBPTamz',
    'access_token_secret': 'NBCNSyXAmQfQWAMQe7qAwPWPdVuhh7HawMdX07tH6R4O1',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
result = bom.check_account('@sophiagdelia')
print(result)

# Check a single account by id
# result = bom.check_account(1548959833)

# Check a sequence of accounts
# accounts = ['@clayadavis', '@onurvarol', '@jabawack']
# for screen_name, result in bom.check_accounts_in(accounts):
#     print(screen_name + '\n' + result)

