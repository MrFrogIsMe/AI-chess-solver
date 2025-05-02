from sys import argv

print(argv)

if __name__ == "__main__":
    task = 0
    m, n = 0, 0
    if len(argv) > 1:
        task = int(argv[1].strip(','))
        m, n = int(argv[2].strip(',')), int(argv[3].strip(','))
    else: 
        with open('input.txt', 'r') as f:
            lines = f.readline().strip().split(',')
            print(lines)
            task = int(lines[0])
            m, n = int(lines[1]), int(lines[2])
    print(task, m, n)
    match(task):
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case _:
            raise ValueError("Invalid task number")
