def Area_circle(radius):
  radius=input(print("Enter the radius"))
  area=3.14*radius*radius

def Area_triangle(base,height):
  base=input(print("Enter the base"))
  height=input(print("Enter the height"))
  return 0.5*base*height

Shape=input(print("Select the shape: Circle or Triangle"))
if Shape==Circle:
  Area_circle()
else:
  Area_triangle();

