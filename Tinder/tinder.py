import mysql.connector

class Tinder:
    def __init__(self):
        #connect to the db
        self.conn=mysql.connector.connect(host='localhost',user='root',password='',database='tinder3')
        self.mycursor=self.conn.cursor()

        self.program_menu()

    def program_menu(self):

        program_input=input("""Hi what would you like to do?
        1.Enter 1 to Create an account
        2.Enter 2 to login
        3.Anything else to exit""")

        if program_input=='1':
            self.register()
        elif program_input=='2':
            self.login()
        else:
            print('Bye')

    def register(self):
        name=input('Name:')
        email=input('Email:')
        password=input('Password:')
        gender=input('Gender:')
        age=input('Age:')
        city=input('City')
        self.mycursor.execute(
            """SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        repeated_email = self.mycursor.fetchall()
        counter=0
        for i in repeated_email:

            email=i
            counter=counter+1
        if counter>0:
                print('Email already exists')
                self.program_menu()
        else:
                self.mycursor.execute(
                    """INSERT INTO `users` (`user_id`,`name`,`email`,`password`,`gender`,`age`,`city`) VALUES (NULL,'{}','{}','{}','{}','{}','{}')""".format(
                        name, email, password, gender, age, city))
                self.conn.commit()
                print('Registration Successful!!!')
                self.program_menu()



    def login(self):
         email=input('Enter email:')
         password=input('Enter password:')


         self.mycursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
         user_list = self.mycursor.fetchall()

         counter=0
         for i in user_list:
             counter=counter+1
             current_user=i
         if counter>0:
             print('Welcome')
             self.current_user_id=current_user[0]
             self.user_menu()
         else:
             print('Incorrect')
    def user_menu(self):
        user_input=input("""How would you like to proceed?
        1.Enter 1 to view users whom you can propose
        2.Enter 2 to view proposals
        3.Enter 3 to view requests
        4.Enter 4 to view matches
        5.Enter 5 to view all users
        6.Anything else to logout""")

        if user_input=='1':
            self.view_users()
        elif user_input=='2':
            self.view_proposals()
        elif user_input=='3':
            self.view_requests()
        elif user_input=='4':
            self.view_matches()
        elif user_input=='5':
            self.view_everything()
        else:
            self.logout()

    def view_users(self):

        self.mycursor.execute("""SELECT * FROM `users` WHERE `user_id` NOT LIKE '{}'""".format(self.current_user_id))

        all_users_list=self.mycursor.fetchall()


        for i in all_users_list:
            print(i[0],'|',i[1],'|',i[4],'|',i[5],'|',i[6])
            print('---------------------')

        self.juliet_id=input('Enter the id of the user whom you want to propose')

        self.propose(self.current_user_id,self.juliet_id)

    def propose(self,romeo_id,juliet_id):

            self.mycursor.execute("""INSERT INTO `proposals`
                    (`proposal_id`,`romeo_id`,`juliet_id`) VALUES (NULL,'{}','{}')""".format(romeo_id, juliet_id))
            self.conn.commit()
            print('Proposal sent successfully.Fingers Crossed')

    def view_proposals(self):
        print('The users whom you have proposed are:')
        self.mycursor.execute("""SELECT * FROM `proposals` p
        JOIN `users` u
        ON u.`user_id`=p.`juliet_id`
        WHERE p.`romeo_id` LIKE '{}'""".format(self.current_user_id))
        proposed_user_list=self.mycursor.fetchall()
        for i in proposed_user_list:
            print(i[4],'|',i[7],'|',i[8],'|',i[9])
            print('---------------------')

    def view_requests(self):
        print('The users who have proposed you:')
        self.mycursor.execute("""SELECT * FROM `proposals` p
               JOIN `users` u
               ON u.`user_id`=p.`romeo_id`
               WHERE p.`juliet_id` LIKE '{}'""".format(self.current_user_id))
        requests_user_list = self.mycursor.fetchall()
        for i in requests_user_list:
            print(i[4], '|', i[7], '|', i[8], '|', i[9])
            print('---------------------')

    def view_matches(self):
        self.mycursor.execute("""SELECT `name`,`gender`,`age`,`city` FROM `users` WHERE `user_id` IN (SELECT `juliet_id` FROM `proposals` WHERE `romeo_id` LIKE '{}' AND `juliet_id`
        IN (SELECT `romeo_id` FROM `proposals` WHERE `juliet_id` LIKE '{}'))""".format(self.current_user_id,self.current_user_id))
        matched_user=self.mycursor.fetchall()
        for i in matched_user:
            print(i[0],i[1],i[2],i[3],sep='|')
            print('---------------------------------')

    def logout(self):
        print('Logged out')
        self.current_user_id=self.program_menu()

user=Tinder()