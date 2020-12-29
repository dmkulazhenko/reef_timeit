# Reef TimeIt

HubStaff reports creator :)

***

## Deployment

### Requirements
* Docker

### FAST! How to start app?
Configure app using ``.env`` file, example: ``example.env``.
File structure described above.
* ``reef_timeit $> MIGRATE=true docker-compose up --build``
  — build + start + migrate db.
* ``reef_timeit $> docker-compose up --build``
  — build + start + run migrations, if something new added to ``migrations``.
* ``reef_timeit $> docker-compouse up``
  — start + run migrations, if something new added to ``migrations``.
  
  
### OK! Now tell me the story...
#### Env vars for docker:
* MIGRATE — Optional[bool] (true/false/none) if ``true`` — DB migrations will
  be executed on start up.
  
#### Configuration files
* ``.env`` — credential / secret keys / tokens.
  If you don't want to used ``.env`` file — just use environment variables
* ``reef_timeit/config.py`` — config for main flask-app.
* ``reef_hub_api/config.py`` — config for HubStaff API Client.
* ``timeit_app.sh`` — start script, you caa modify workers/threads num.

#### .env file (environment variables) structure
* SECRET_KEY = secret-key-for-flask-tools

* MYSQL_ROOT_PASSWORD = password-for-root-user-of-database
* MYSQL_USER = username-of-reef-timeit-database-user
* MYSQL_DATABASE = database-name-for-reef-timeit
* MYSQL_PASSWORD = password-of-reef-timeit-database-user

* HUB_APP_TOKEN = token-from-hubstaff-v1-api
* HUB_EMAIL = email-from-hubstaff
* HUB_PASSWORD = password-from-habstaff

To use ``.env`` file configuration – create file ``.env`` in project root dir.
Example of ``.env`` file — ``example.env``

***

## Summary about the task:

*Well-known old friend is better than anything narrow-profile and new.*

The task was pretty interesting, I liked working with it.
I hope that you will also enjoy reviewing my code.
In general, I used flask + docker for this task, since
I don't see the point of writting asynchronous code or anything like that.

### Main points:
* Table can be generated for any range of time,
  using ``/?start_time=<timestamp>&stop_time=<timestamp>``.
* You can save table to csv file (idk, should I do it or not),
  but in the task ``The output should saved to a file``.
* Data from hubstaff fetches every 15 minutes,
  btw if you need data right now just use button.
* Easy to add email using flask-mail and dummy threading :)

### Shortcomings:
* Work with timezones on frontend + yesterday is UTC yesterday, not your local.
  This can be easy fixed via normal frontend as far as app has timestamps param.
  I won't do it, bcs I will be backend developer, not frontend :) 
* Fetch by the button doesn't async, can be fixed
  using multiprocessing or something like that.
  At all, I think, that this realization enough for this kind of project,
  as far as timeout set to 90...
* Frontend part is bad at all, again for *backend* tasks :) 
* No documentation and tests
