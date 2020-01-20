class User:
    def __str__(self):
        return ' name: ' + self.name


if __name__ == '__main__':
    u = User()
    u.name = 'Wang'
    print(u)