import util.gmaps as gmaps

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def get_solution(data):

  manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'], data['ends'])
  
  routing = pywrapcp.RoutingModel(manager)

  # Constante distancia
  def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

  transit_callback_index = routing.RegisterTransitCallback(distance_callback)

  routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


  # Constante capacidad
  def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

  demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
  
  routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # slack
        data['vehicle_capacities'],  # Maximas Capacidades
        True,  # Empezar a acumular desde 0
        'Capacity')

  # Heuristica
  search_parameters = pywrapcp.DefaultRoutingSearchParameters()
  search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
  search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
  search_parameters.time_limit.FromSeconds(1)

  # Solucionar el problema
  solution = routing.SolveWithParameters(search_parameters)

  return (solution, manager, routing)


def get_full_route(data, manager, routing, solution, df_drivers):
    
  answer = []
  
  for vehicle_id in range(data['num_vehicles']):
    index = routing.Start(vehicle_id)
    plan_output = 'Ruta del vehiculo {}:\n'.format(vehicle_id)
    # id, distance, license_plate, driver, route(matrix)
    
    route = []
    lon = df_drivers.lng[vehicle_id]
    lat =  df_drivers.lat[vehicle_id]

    route_distance = 0
    route_load = 0

    plan_output = ""
    while not routing.IsEnd(index):
      node_index = manager.IndexToNode(index)
      route_load += data['demands'][node_index]

      lon = data['longitudes'][node_index]
      lat = data['latitudes'][node_index]
      route.append([ lat, lon ])

      plan_output += ' {0} Carga({1}) -> '.format(node_index, route_load)
      previous_index = index
      index = solution.Value(routing.NextVar(index))
      route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        
    
    plan_output += ' {0} Carga({1})\n'.format(manager.IndexToNode(index), route_load)
    
    lon = data['longitudes'][manager.IndexToNode(index)]
    lat = data['latitudes'][manager.IndexToNode(index)]
    
    print(plan_output)

    route.append( [lat, lon] )   

    full_route = []

    for i in range(len(route) - 1):
      full_route+= gmaps.get_route_points(route[i][0], route[i][1], route[i+1][0], route[i+1][1])
      

    elem = {
      'id': df_drivers.id[vehicle_id],
      'distance' : route_distance,
      'license_plate' : df_drivers.license_plate[vehicle_id],
      'route': full_route
    }

    answer.append(elem)
  

  return answer