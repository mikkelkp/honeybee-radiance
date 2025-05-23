from honeybee_radiance.lightpath import light_path_from_room
from honeybee_radiance.sensorgrid import SensorGrid
from honeybee_radiance.view import View

from honeybee.room import Room
from honeybee.model import Model
from ladybug_geometry.geometry3d.pointvector import Point3D


def test_light_path_from_room_interior():
    """Test the light_path_from_room method with interior apertures."""
    room1 = Room.from_box('Tiny_House_Room1', 5, 10, 3)
    room1[2].apertures_by_ratio(0.4, 0.01)  # east interior window
    room1[3].apertures_by_ratio(0.4, 0.01)  # outdoor south window
    south_ap1 = room1[3].apertures[0]
    south_ap1.properties.radiance.dynamic_group_identifier = 'SouthWindow1'

    room2 = Room.from_box('Tiny_House_Room2', 5, 10, 3, origin=Point3D(5, 0, 0))
    room2[4].apertures_by_ratio(0.4, 0.01)  # west interior window
    room2[1].apertures_by_ratio(0.4, 0.01)  # outdoor north window
    north_ap2 = room2[1].apertures[0]
    north_ap2.properties.radiance.dynamic_group_identifier = 'NorthWindow2'

    Room.solve_adjacency([room1, room2], 0.01)
    model = Model('TinyHouse', [room1, room2])

    lp = light_path_from_room(model, room1.identifier)
    assert ['SouthWindow1'] in lp
    assert ['__static_apertures__', 'NorthWindow2'] in lp

    room1[1].apertures_by_ratio(0.4, 0.01)  # outdoor north window
    lp = light_path_from_room(model, room1.identifier)
    assert ['SouthWindow1'] in lp
    assert ['__static_apertures__'] in lp
    assert ['__static_apertures__', 'NorthWindow2'] in lp


def test_grid_and_view_info_dict():
    """Test the info_dict methods on SensorGrid and View."""
    room1 = Room.from_box('Tiny_House_Room', 5, 10, 3)
    room1[3].apertures_by_ratio(0.4, 0.01)
    south_ap1 = room1[3].apertures[0]
    south_ap1.properties.radiance.dynamic_group_identifier = 'SouthWindow1'

    room2 = Room.from_box('Tiny_House_Room', 5, 10, 3, origin=Point3D(5, 0, 0))
    room2[3].apertures_by_ratio(0.4, 0.01)
    south_ap2 = room2[3].apertures[0]
    south_ap2.properties.radiance.dynamic_group_identifier = 'SouthWindow2'

    sensor_grid = room1.properties.radiance.generate_sensor_grid(0.5, 0.5, 1)

    assert isinstance(sensor_grid, SensorGrid)
    assert sensor_grid.room_identifier == room1.identifier
    assert len(sensor_grid.sensors) == 5 * 10 * 4

    model = Model('TinyHouse', [room1, room2])

    folder_dict = sensor_grid.info_dict(model)
    assert folder_dict['count'] == len(sensor_grid.sensors)
    assert folder_dict['light_path'] == [['SouthWindow1']]

    sensor_grid.light_path = [['SouthWindow1'], ['SouthWindow2']]
    folder_dict = sensor_grid.info_dict(model)
    assert folder_dict['light_path'] == [['SouthWindow1'], ['SouthWindow2']]

    view = View('test_view', (2.5, 5, 1.5), (0, -1, 0))
    view.room_identifier = room1.identifier
    folder_dict = view.info_dict(model)
    assert folder_dict['light_path'] == [['SouthWindow1']]

    view.light_path = [['SouthWindow1'], ['SouthWindow2']]
    folder_dict = view.info_dict(model)
    assert folder_dict['light_path'] == [['SouthWindow1'], ['SouthWindow2']]


room_light_path_dict = {
    'room_1': [
        ['__static_apertures__'],
        ['room_1_south'],
        ['__static_apertures__', 'room_2_east'],
        ['__static_apertures__', 'room_3-4_west', 'room_4_east'],
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__', 'room_5_west'],
        ['__static_apertures__', 'room_3-4_west', 'room_4-5', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_west', 'room_4-5', 'room_5_west'],
        ['__static_apertures__', 'room_3-4_east', 'room_4_east'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__', 'room_5_west'],
        ['__static_apertures__', 'room_3-4_east', 'room_4-5', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', 'room_4-5', 'room_5_west'],
        ['room_1-2', 'room_2_east'],
        ['room_1-2', 'room_3-4_west', 'room_4_east'],
        ['room_1-2', 'room_3-4_west', '__static_apertures__'],
        ['room_1-2', 'room_3-4_west', '__static_apertures__', 'room_5_west'],
        ['room_1-2', 'room_3-4_west', 'room_4-5', '__static_apertures__'],
        ['room_1-2', 'room_3-4_west', 'room_4-5', 'room_5_west'],
        ['room_1-2', 'room_3-4_east', 'room_4_east'],
        ['room_1-2', 'room_3-4_east', '__static_apertures__'],
        ['room_1-2', 'room_3-4_east', '__static_apertures__', 'room_5_west'],
        ['room_1-2', 'room_3-4_east', 'room_4-5', '__static_apertures__'],
        ['room_1-2', 'room_3-4_east', 'room_4-5', 'room_5_west'],
        ['room_1-2', '__static_apertures__']
    ],
    'room_2': [
        ['__static_apertures__'],
        ['__static_apertures__', 'room_1_south'],
        ['room_1-2', '__static_apertures__'],
        ['room_1-2', 'room_1_south'],
        ['room_2_east'],
        ['room_3-4_west', 'room_4_east'],
        ['room_3-4_west', '__static_apertures__'],
        ['room_3-4_west', '__static_apertures__', 'room_5_west'],
        ['room_3-4_west', 'room_4-5', '__static_apertures__'],
        ['room_3-4_west', 'room_4-5', 'room_5_west'],
        ['room_3-4_east', 'room_4_east'],
        ['room_3-4_east', '__static_apertures__'],
        ['room_3-4_east', '__static_apertures__', 'room_5_west'],
        ['room_3-4_east', 'room_4-5', '__static_apertures__'],
        ['room_3-4_east', 'room_4-5', 'room_5_west']
    ],
    'room_3': [
        ['__static_apertures__'],
        ['__static_apertures__', 'room_1_south'],
        ['room_1-2', '__static_apertures__'],
        ['room_1-2', 'room_1_south'],
        ['room_2_east'],
        ['room_3-4_west', 'room_4_east'],
        ['room_3-4_west', '__static_apertures__'],
        ['room_3-4_west', '__static_apertures__', 'room_5_west'],
        ['room_3-4_west', 'room_4-5', '__static_apertures__'],
        ['room_3-4_west', 'room_4-5', 'room_5_west'],
        ['room_3-4_east', 'room_4_east'],
        ['room_3-4_east', '__static_apertures__'],
        ['room_3-4_east', '__static_apertures__', 'room_5_west'],
        ['room_3-4_east', 'room_4-5', '__static_apertures__'],
        ['room_3-4_east', 'room_4-5', 'room_5_west']
    ],
    'room_4': [
        ['room_3-4_west', '__static_apertures__'],
        ['room_3-4_west', '__static_apertures__', 'room_1_south'],
        ['room_3-4_west', 'room_1-2', '__static_apertures__'],
        ['room_3-4_west', 'room_1-2', 'room_1_south'],
        ['room_3-4_west', 'room_2_east'],
        ['room_3-4_west', '__static_apertures__'],
        ['room_3-4_east', '__static_apertures__'],
        ['room_3-4_east', '__static_apertures__', 'room_1_south'],
        ['room_3-4_east', 'room_1-2', '__static_apertures__'],
        ['room_3-4_east', 'room_1-2', 'room_1_south'],
        ['room_3-4_east', 'room_2_east'],
        ['room_3-4_east', '__static_apertures__'],
        ['room_4_east'],
        ['__static_apertures__'],
        ['__static_apertures__', 'room_5_west'],
        ['room_4-5', '__static_apertures__'],
        ['room_4-5', 'room_5_west']
    ],
    'room_5': [
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_west', 'room_1-2', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_west', 'room_1-2', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_west', 'room_2_east'],
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_east', 'room_1-2', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', 'room_1-2', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_east', 'room_2_east'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__'],
        ['__static_apertures__', 'room_4_east'],
        ['room_4-5', 'room_3-4_west', '__static_apertures__'],
        ['room_4-5', 'room_3-4_west', '__static_apertures__', 'room_1_south'],
        ['room_4-5', 'room_3-4_west', 'room_1-2', '__static_apertures__'],
        ['room_4-5', 'room_3-4_west', 'room_1-2', 'room_1_south'],
        ['room_4-5', 'room_3-4_west', 'room_2_east'],
        ['room_4-5', 'room_3-4_west', '__static_apertures__'],
        ['room_4-5', 'room_3-4_east', '__static_apertures__'],
        ['room_4-5', 'room_3-4_east', '__static_apertures__', 'room_1_south'],
        ['room_4-5', 'room_3-4_east', 'room_1-2', '__static_apertures__'],
        ['room_4-5', 'room_3-4_east', 'room_1-2', 'room_1_south'],
        ['room_4-5', 'room_3-4_east', 'room_2_east'],
        ['room_4-5', 'room_3-4_east', '__static_apertures__'],
        ['room_4-5', 'room_4_east'],
        ['__static_apertures__'],
        ['room_5_west']
    ],
    'room_6': [
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_west', 'room_1-2', '__static_apertures__'], 
        ['__static_apertures__', 'room_3-4_west', 'room_1-2', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_west', 'room_2_east'],
        ['__static_apertures__', 'room_3-4_west', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_east', 'room_1-2', '__static_apertures__'],
        ['__static_apertures__', 'room_3-4_east', 'room_1-2', 'room_1_south'],
        ['__static_apertures__', 'room_3-4_east', 'room_2_east'],
        ['__static_apertures__', 'room_3-4_east', '__static_apertures__'],
        ['__static_apertures__', 'room_4_east'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_west', '__static_apertures__'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_west', '__static_apertures__', 'room_1_south'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_west', 'room_1-2', '__static_apertures__'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_west', 'room_1-2', 'room_1_south'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_west', 'room_2_east'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_west', '__static_apertures__'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_east', '__static_apertures__'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_east', '__static_apertures__', 'room_1_south'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_east', 'room_1-2', '__static_apertures__'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_east', 'room_1-2', 'room_1_south'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_east', 'room_2_east'],
        ['__static_apertures__', 'room_4-5', 'room_3-4_east', '__static_apertures__'],
        ['__static_apertures__', 'room_4-5', 'room_4_east'],
        ['__static_apertures__'],
        ['__static_apertures__', 'room_5_west'],
        ['room_5-6', '__static_apertures__', 'room_3-4_west', '__static_apertures__'],
        ['room_5-6', '__static_apertures__', 'room_3-4_west', '__static_apertures__', 'room_1_south'],
        ['room_5-6', '__static_apertures__', 'room_3-4_west', 'room_1-2', '__static_apertures__'],
        ['room_5-6', '__static_apertures__', 'room_3-4_west', 'room_1-2', 'room_1_south'],
        ['room_5-6', '__static_apertures__', 'room_3-4_west', 'room_2_east'],
        ['room_5-6', '__static_apertures__', 'room_3-4_west', '__static_apertures__'],
        ['room_5-6', '__static_apertures__', 'room_3-4_east', '__static_apertures__'],
        ['room_5-6', '__static_apertures__', 'room_3-4_east', '__static_apertures__', 'room_1_south'],
        ['room_5-6', '__static_apertures__', 'room_3-4_east', 'room_1-2', '__static_apertures__'],
        ['room_5-6', '__static_apertures__', 'room_3-4_east', 'room_1-2', 'room_1_south'],
        ['room_5-6', '__static_apertures__', 'room_3-4_east', 'room_2_east'],
        ['room_5-6', '__static_apertures__', 'room_3-4_east', '__static_apertures__'],
        ['room_5-6', '__static_apertures__', 'room_4_east'],
        ['room_5-6', 'room_4-5', 'room_3-4_west', '__static_apertures__', '__static_apertures__'],
        ['room_5-6', 'room_4-5', 'room_3-4_west', '__static_apertures__', 'room_1_south'],
        ['room_5-6', 'room_4-5', 'room_3-4_west', 'room_1-2', '__static_apertures__'],
        ['room_5-6', 'room_4-5', 'room_3-4_west', 'room_1-2', 'room_1_south'],
        ['room_5-6', 'room_4-5', 'room_3-4_west', 'room_2_east'],
        ['room_5-6', 'room_4-5', 'room_3-4_west', '__static_apertures__'],
        ['room_5-6', 'room_4-5', 'room_3-4_east', '__static_apertures__', '__static_apertures__'],
        ['room_5-6', 'room_4-5', 'room_3-4_east', '__static_apertures__', 'room_1_south'],
        ['room_5-6', 'room_4-5', 'room_3-4_east', 'room_1-2', '__static_apertures__'],
        ['room_5-6', 'room_4-5', 'room_3-4_east', 'room_1-2', 'room_1_south'],
        ['room_5-6', 'room_4-5', 'room_3-4_east', 'room_2_east'],
        ['room_5-6', 'room_4-5', 'room_3-4_east', '__static_apertures__'],
        ['room_5-6', 'room_4-5', 'room_4_east'],
        ['room_5-6', '__static_apertures__'],
        ['room_5-6', 'room_5_west']
    ]
}

def test_large_light_path_model():
    """Test the large light path model with multiple interior Apertures."""
    model = Model.from_hbjson('./tests/assets/model/large_light_path_model.hbjson')
    for room in model.rooms:
        room_display_name = room.display_name
        light_path = light_path_from_room(model, room.identifier)

        check_light_path = room_light_path_dict[room_display_name]
        for lp in light_path:
            assert lp in check_light_path
