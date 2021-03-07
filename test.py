import os
 
env_var_name = 'SECRET_KEY'
env_var_value = 'YaredYeArsemaLij'
if env_var_name not in os.environ:
    os.environ[env_var_name] = env_var_value
print(os.environ[env_var_name])