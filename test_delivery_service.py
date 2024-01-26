import random
from delivery_service import DeliveryService


if __name__ == '__main__':
    print("--------- Task1 load map ---------")
    
    ds = DeliveryService()
    ds.buildMap('city_map_5.txt')
    print("Loaded {} vertices".format(ds.city_map.numVertices))

    print("--------- Task2 check if within service range ---------")
    number_nodes = 3
    random_nodes = [v.id for v in random.sample(list(ds.city_map.vertList.values()), number_nodes)]
    threshold = 10
    for i in range(number_nodes - 1):
        print('Restaurant:', random_nodes[i], ', User:', random_nodes[i+1], 'within service range (' + str(threshold) + ')?:', ds.isWithinServiceRange(random_nodes[i], random_nodes[i+1], 10))

    print("--------- Task3 build MST ---------")
    ds.buildMST(0)
    print('MST number of nodes:', ds.MST.numVertices)
    print('MST total edge weights:', DeliveryService.totalEdgeWeight(ds.MST))

    print("--------- Task4 find path in MST ---------")
    for i in range(number_nodes - 1):
        print("From", random_nodes[i], "to", random_nodes[i+1], 'delivery time:', ds.minimalDeliveryTime(random_nodes[i], random_nodes[i+1]))

    print("--------- Task5 find delivery path ---------")
    for i in range(number_nodes - 1):
        print("From", random_nodes[i], "to", random_nodes[i+1], 'Path:', ds.findDeliveryPath(random_nodes[i], random_nodes[i+1]))

    print("--------- Task6 find delivery path given delay ---------")
    for i in range(number_nodes - 1):
        restaurant = random_nodes[i]
        user = random_nodes[i+1]
        delayed_nodes = random.choices(list(ds.city_map.vertList.values()), k=3)
        delay_info = {}
        for d in delayed_nodes:
            delay_info[d.id] = random.randint(1, 10)
        try:
            del delay_info[restaurant]
        except:
            pass
        try:
            del delay_info[user]
        except:
            pass
        print("Delay info:", delay_info)
        print(restaurant, user, 'Path:', ds.findDeliveryPathWithDelay(restaurant, user, delay_info))