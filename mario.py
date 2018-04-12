import cs50, sys

def main():
    height = get_arg()
    if not height is None:
        draw_pyramids(height)
    
def get_arg():
    if len(sys.argv) != 2 or int(sys.argv[1]) > 23 or int(sys.argv[1]) < 0:
        return
    return int(sys.argv[1])
    
def draw_pyramids(pyH):
    for i in range(pyH):
        draw_left(pyH, i)
        print("  ", end="", flush=True)
        draw_right(i)
        print("\n")
        
def draw_left(pyH, i):
    for j in range(pyH-i):
        print(" ", end="", flush=True)
    
    for i in range(i):
        print("#", end="", flush=True)
    
def draw_right(i):
    for i in range(i):
        print("#", end="", flush=True)
        True
    
if __name__ == "__main__":
    main()