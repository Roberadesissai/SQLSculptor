import bcrypt

def encript(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

if __name__ == '__main__':
    print(encript('Grace#8741'))
    print(check_password('Grace#8741', '$2b$12$VC3a2UC4SzuMPzPIyAm3p.UiDsetY50Y1LQs0HCNIyCidBaOTeTeW'))
