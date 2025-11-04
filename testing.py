def area_circle(radius):
    """Calculate the area of a circle given its radius."""
    area = 3.14159 * radius * radius
    return area

def area_triangle(base, height):
    """Calculate the area of a triangle given its base and height."""
    area = 0.5 * base * height
    return area

def main():
    """Main function to run the shape area calculator."""
    print("=== Shape Area Calculator ===")
    print("Select a shape:")
    print("1. Circle")
    print("2. Triangle")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        try:
            radius = float(input("Enter the radius: "))
            if radius < 0:
                print("Error: Radius cannot be negative!")
            else:
                result = area_circle(radius)
                print(f"Area of circle: {result:.2f}")
        except ValueError:
            print("Error: Please enter a valid number!")
    
    elif choice == "2":
        try:
            base = float(input("Enter the base: "))
            height = float(input("Enter the height: "))
            if base < 0 or height < 0:
                print("Error: Base and height cannot be negative!")
            else:
                result = area_triangle(base, height)
                print(f"Area of triangle: {result:.2f}")
        except ValueError:
            print("Error: Please enter valid numbers!")
    
    else:
        print("Invalid choice! Please select 1 or 2.")

if __name__ == "__main__":
    main()
