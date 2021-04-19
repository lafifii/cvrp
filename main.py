import util.model as model
import util.solver as solver

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def graphic_routes(answer):

  def route_split(route):
    xs = []
    ys = []
    for z in route:
      xs.append(z[0])
      ys.append(z[1])
    
    return xs, ys

  xs = []
  ys = []

  color = ['blue', 'red', 'yellow', 'orange', 'green', 'cyan']
  cli = 0

  for z in answer:
    prevx = -1
    prevy = -1

    for i in range(len(z['route'])):
      
      xs.append(z['route'][i][0])
      ys.append(z['route'][i][1])

      if(i > 0):
        x_values = [prevx, xs[-1]]
        y_values = [prevy, ys[-1]]
        
        plt.plot(x_values, y_values, color=color[cli])
      
      prevx, prevy = xs[-1], ys[-1]
    
    cli+=1
    
  plt.scatter(xs, ys)  


if __name__ == "__main__":

  df_drivers, df_locations = model.load_data('sample_data/drivers.txt', 'sample_data/locations.txt')

  data = model.create_model(df_drivers, df_locations)

  print(data)

  solution, manager, routing = solver.get_solution(data)

  if(solution):
    answer = solver.get_full_route(data,manager,routing,solution,df_drivers)
    graphic_routes(answer)

  else:
    print("No Solution")


