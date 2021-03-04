import logging
import pyodbc
import os
import azure.functions as func
import json
import redis

<<<<<<< HEAD
CACHE_TOGGLE= os.environ["CACHE_TOGGLE"]
=======
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef

# This is the Http Trigger for Users/userId
# It connects to the db and retrives the users added to the db by userId
def main(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    user_id = req.route_params.get('userId')

    logging.info(
      '''
        Python HTTP trigger for users/userId is
        processing a request to get user with id {}
      '''.format(user_id)
    )

<<<<<<< HEAD
    #Initiating REDIS cache
    rDBHost = os.environ["ENV_REDIS_HOST"]
    rDBPort = os.environ["ENV_REDIS_PORT"]
    r = redis.Redis(host= rDBHost, port= rDBPort, db= 0, password= '${{ secrets.ENV_REDIS_KEY }}', ssl= True)

=======
    # Create a new connection
    logging.debug('Attempting DB connection!')
    try:
        conn = get_db_connection()
    except (pyodbc.DatabaseError, pyodbc.InterfaceError) as e:
        logging.critical('Failed to connect to DB: ' + e.args[0])
        logging.info('Error: ' + e.args[1])
        return func.HttpResponse(status_code=500)

    logging.debug('Connection to DB successful!')
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef

    try:
        _redis = init_redis()
        # Return results according to the method
        if method == 'GET':
            logging.info('Attempting to retrieve user...')
            user_http_response = get_user(conn, user_id, _redis)
            logging.info('User retrieved successfully!')
            return user_http_response
        elif req.method == 'PUT':
            user_req_body = get_user_req_body(req)

            logging.info('Attempting to update (PUT) user...')

            return update_user(user_req_body, conn, user_id, _redis)
        elif req.method == 'PATCH':
            user_req_body = get_user_req_body(req)

            logging.info('Attempting to update (PATCH) user...')

            return patch_user(user_req_body, conn, user_id, _redis)
        elif method == 'DELETE':
            logging.info('Attempting to delete user...')

            return delete_user(conn, user_id, _redis)
        else:
            logging.warn('''
              Request with method {} has been recieved,
              but that is not allowed for this endpoint
            '''.format(method))

            return func.HttpResponse('invalid request method', status_code=405)

    # displays erros encountered when API methods were called
    except Exception as e:
        return func.HttpResponse('Error: %s' % str(e), status_code=500)
    finally:
        conn.close()
        logging.debug('Connection to DB closed')


def get_db_connection():
    # Connection String
    connection_string = os.environ['ENV_DATABASE_CONNECTION_STRING']

    return pyodbc.connect(connection_string)


def init_redis():
    REDIS_HOST = 'nsc-redis-dev-usw2-thursday.redis.cache.windows.net'
    REDIS_KEY = os.environ['ENV_REDIS_KEY']

    return redis.StrictRedis(
      host=REDIS_HOST, port=6380, db=0, password=REDIS_KEY, ssl=True
    )


def get_user(conn, user_id, _redis):
    try:
<<<<<<< HEAD
        cache = get_user_id_cache(r, user_id)
    except TypeError as e:
        logging.info(e.args[0])
    if cache:
        logging.info("Data returned from cache")
        return func.HttpResponse(cache.decode('utf-8'), status_code =200, mimetype="application/json")
    else:
        if(CACHE_TOGGLE == "On")
            logging.info("Empty cache, querying...")
        sql_query = ("""SELECT CONCAT (users.firstName, ' ', users.lastName) AS "user",
                        FROM [dbo].[users] 
                        WHERE [dbo].[users].userId = ?""")
        cursor.execute(sql_query, user_id)
=======
        cache = get_user_cache(_redis)
        user = json.loads(cache)
        user_user_id = user['userId']
        is_cachable = cache is not None and int(user_user_id) == int(user_id)
    except TypeError as e:
        logging.info(e.args[0])
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef

    try:
        if (cache is None) or not is_cachable:
            with conn.cursor() as cursor:
                logging.debug(
                    '''
                      Using connection cursor to execute query
                      (select user from users)
                    '''
                )

                cursor.execute('SELECT * FROM users WHERE userId = ?', user_id)

                # Get user
                logging.debug('Fetching all queried information')
                user_data = list(cursor.fetchone())
                columns = [column[0] for column in cursor.description]
                user = dict(zip(columns, user_data))

                logging.debug(
                    '''
                      User data retrieved and processed,
                      returning information from get_users function
                    '''
                  )

                logging.info('Caching results...')

<<<<<<< HEAD
    #Caches the User ID data
    cache_user_id(r, user_id, users)

    return func.HttpResponse(
        json.dumps(user_id_data),
        status_code=200,
        mimetype="application/json"
    )
=======
                # Cache the results
                cache_user(_redis, user)

                respond = json.dumps(user)
                statuse_code = 200
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef

        if cache is not None:
            respond = cache.decode('utf-8')
            statuse_code = 200

    except TypeError as e:
        respond = 'get user failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

    return func.HttpResponse(
        respond,
        status_code=statuse_code,
        mimetype='application/json'
    )


def get_user_cache(_redis):
    try:
        cache = _redis.get('user')
        return cache
    except TypeError as e:
        logging.critical('Failed to fetch user from cache: ' + e.args[1])
        return None


def set_user_cache(_redis, clear_cache):
    if clear_cache:
        _redis.flushdb()


def cache_user(_redis, user):
    try:
        _redis.set('user', json.dumps(user), ex=1200)
        logging.info('Caching complete')
    except TypeError as e:
        logging.info('Caching failed')
        logging.info(e.args[0])


def update_user(user_req_body, conn, user_id, _redis):
    # Validate request body
    logging.debug('Verifying fields in request body to update a user by ID')
    try:
<<<<<<< HEAD
        cache = put_user_id_cache(r, user_id)
        assert "firstName" in user_req_body, "User request body did not contain field: 'firstName'"
        assert "lastName" in user_req_body, "User request body did not contain field: 'lastName'"
        assert "email" in user_req_body, "User request body did not contain field: 'email'"
=======
        assert 'firstName' in user_req_body, 'User request body did not contain field: "firstName"'
        assert 'lastName' in user_req_body, 'User request body did not contain field: "lastName"'
        assert 'email' in user_req_body, 'User request body did not contain field: "email"'
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef
    except AssertionError as user_req_body_content_error:
        logging.error(e.args[0])
        logging.error(
<<<<<<< HEAD
            "User request body did not contain the necessary fields!")
        return func.HttpResponse(user_req_body_content_error.args[0], status_code=400)
    logging.debug("User request body contains all the necessary fields!")

    # Unpack user data
    firstName = user_req_body["firstName"]
    lastName = user_req_body["lastName"]
    email = user_req_body["email"]

    if cache:
        logging.info("Data returned from cache")
        return func.HttpResponse(cache.decode('utf-8'), status_code =200, mimetype="application/json")        
    else:
        # Update user in DB
        update_user_query = "UPDATE dbo.users SET firstName = ?, lastName = ?, email = ? WHERE userId= ?"
        logging.debug("Executing query: " + update_user_query)
        cursor.execute(update_user_query,
                   (firstName, lastName, email, user_id))
        logging.debug("User was updated successfully!.")
        logging.debug("Fetching new entries...")
        new_user_id_table = list(cursor.fetchall())
        #Cleans data to put into cache
        new_user_id_data = [tuple(user_id) for user_id in new_user_id_table]
        #Initialize empty list
        new_user_id_list = []
        #Add data to empty list
        new_user_id_columns = [column[0] for column in cursor.description]
        for user_id in new_user_id_data:
            #Initialize validation method for duplicate user_id into cache
            isDuplicate = duplicate_cache(r, user_id)
            if(isDuplicate == False)
                new_user_id_list.append(dict(zip(columns, row))) 
        logging.debug("New User placed sucessfully!")

        #Cache the data
        cache_user_id(r, user_id, users)

        return func.HttpResponse(
            "User updated",
            status_code=200
        )
=======
            'User request body did not contain the necessary fields!'
        )
        return func.HttpResponse(
          user_req_body_content_error.args[0], status_code=400
        )

    logging.debug('User request body contains all the necessary fields!')

    try:
        with conn.cursor() as cursor:
            # Unpack user data
            firstName = user_req_body['firstName']
            lastName = user_req_body['lastName']
            email = user_req_body['email']

            # Update user in DB
            update_user_query = '''
              UPDATE dbo.users SET firstName = ?,
              lastName = ?, email = ? WHERE userId= ?
            '''

            logging.debug('Executing query: ' + update_user_query)

            cursor.execute(
              update_user_query, (firstName, lastName, email, user_id)
            )

            logging.debug('User was updated successfully!.')

            set_user_cache(_redis, True)
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef

            respond = 'User updated'
            statuse_code = 200

    except TypeError as e:
        respond = 'patch failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

<<<<<<< HEAD
def delete(cursor, user_id):
    logging.debug("Attempting to retrieve user by ID and delete the user...")
    delete_user_query = "DELETE FROM dbo.users  WHERE userId= ?"
    logging.debug("Executing query: " + delete_user_query)
    cursor.execute(delete_user_query, (user_id,))
    logging.debug("User was deleted successfully!.")
    try:
        delete_user_id_cache(r,user_id)
    except TypeError as e:
        logging.error(e.args[0])
=======
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef
    return func.HttpResponse(
        respond,
        status_code=statuse_code
    )


def patch_user(user_req_body, conn, user_id, _redis):
    logging.debug('''
      Going to execute PATCH query on user {}
    '''.format(user_id))

    fieldsToUpdate = list(user_req_body.keys())
    updatableFields = ['firstName', 'lastName', 'email']

<<<<<<< HEAD
#This method caches user_id
#param: r- redis cache
#user_id: User IDs that need to cached
def cache_user_id(r, user_id, users):
    key = "users:" + user_id
    if(CACHE_TOGGLE == "On"):
        try:
            r.set(key, json.dumps(users), ex= 1200) 
            logging.info("Caching complete!")
        except TypeError as e:
            logging.info("Caching failed")
            logging.info(e.args[0])

#This method retrieves the user_id cache
#param: r- Redis Cache that it the user_id cache residing in
def get_user_id_cache(r, user_id):
    logging.info("Querying for User ID cache...")
    try:
        key = "users:" + user_id
        cache = r.get(key)
        return cache
    except TypeError as e:
        logging.critical("Failed to fetch from cache: " + e.args[1])
        return None


def duplicate_cache(r, user_id):
    if user_id is in r:
        return true
    else
        return false

def delete_user_id_cache(r, user_id):
    if user_id is in r:
        key = "users: " + user_id
        r.delete(key)
    else
        logging.critical("This cannot be done as user id does not exist")
=======
    try:
        with conn.cursor() as cursor:
            if len(fieldsToUpdate) == 0:
                logging.critical('''
                  request body did not contain fields to update the user
                ''')

                respond = 'no field to update'
                statuse_code = 400

            elif set(fieldsToUpdate).issubset(updatableFields):
                fieldsInQuery = ''
                params = []

                for field in fieldsToUpdate:
                    comma = ' ' if field == fieldsToUpdate[-1] else ', '
                    params.append(user_req_body[field])

                    fieldsInQuery += "{} = ?{}".format(str(field), comma)

                sql_query = """
                  UPDATE users SET {} WHERE userId = ?
                """.format(fieldsInQuery)

                params.append(int(user_id))

                cursor.execute(sql_query, tuple(params))

                set_user_cache(_redis, True)

                respond = 'user updated successfully'
                statuse_code = 200

            else:
                respond = 'invalid request body'
                statuse_code = 400

    except TypeError as e:
        respond = 'patch failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

    return func.HttpResponse(
        respond,
        status_code=statuse_code
    )


def delete_user(conn, user_id, _redis):
    try:
        with conn.cursor() as cursor:
            logging.debug('''
              Attempting to retrieve user by ID and delete the user...
            ''')

            delete_user_query = 'DELETE FROM users WHERE userId= ?'

            logging.debug('Executing query: ' + delete_user_query)

            cursor.execute(delete_user_query, (user_id))

            logging.debug('User was deleted successfully!.')

            cache = get_user_cache(_redis)
            user = json.loads(cache)
            is_clearable = cache is not None and int(user['userId']) == int(user_id)

            if is_clearable:
                set_user_cache(_redis, True)

            respond = 'User deleted'
            statuse_code = 200
    except TypeError as e:
        respond = 'delete failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

    return func.HttpResponse(respond, status_code=statuse_code)


def get_user_req_body(req):
    user_req_body = dict()

    try:
        user_req_body = req.get_json()
    except ValueError:
        logging.error('Empty req body or non-JSON file passed')
        pass

    return user_req_body
>>>>>>> 94cb1ce615d6d2d1893109d32d78b60c8c12afef
